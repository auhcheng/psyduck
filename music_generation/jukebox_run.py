import jukebox
import torch as t
import librosa
import os
from IPython.display import Audio
from jukebox.make_models import make_vqvae, make_prior, MODELS, make_model
from jukebox.hparams import Hyperparams, setup_hparams
from jukebox.sample import sample_single_window, _sample, \
                           sample_partial_window, upsample, \
                           load_prompts
from jukebox.utils.dist_utils import setup_dist_from_mpi
from jukebox.utils.torch_utils import empty_cache



rank, local_rank, device = setup_dist_from_mpi()


model = '1b_lyrics' # or '5b' or '1b_lyrics'
hps = Hyperparams()
hps.sr = 44100
hps.n_samples = 1 if model in ('5b', '5b_lyrics') else 3
# Specifies the directory to save the sample in.
# We set this to the Google Drive mount point.
hps.name = './samples'
chunk_size = 10 if model in ('5b', '5b_lyrics') else 16
max_batch_size = 2 if model in ('5b', '5b_lyrics') else 3
hps.levels = 3
hps.hop_fraction = [.5,.5,.125]

vqvae, *priors = MODELS[model]
vqvae = make_vqvae(setup_hparams(vqvae, dict(sample_length = 1048576)), device)
top_prior = make_prior(setup_hparams(priors[-1], dict()), vqvae, device)


# Prime song creation using an arbitrary audio sample.
mode = 'primed'
codes_file=None
# Specify an audio file here.
audio_file = './neg_bg_music_short.wav'
# Specify how many seconds of audio to prime on.
prompt_length_in_seconds=14


if os.path.exists(hps.name):
  # Identify the lowest level generated and continue from there.
  for level in [1, 2]:
    data = f"{hps.name}/level_{level}/data.pth.tar"
    if os.path.isfile(data):
      mode = 'upsample'
      codes_file = data
      print('Upsampling from level '+str(level))
      break
print('mode is now '+mode)

sample_hps = Hyperparams(dict(mode=mode, codes_file=codes_file, audio_file=audio_file, prompt_length_in_seconds=prompt_length_in_seconds))

sample_length_in_seconds = 50          # Full length of musical sample to generate - we find songs in the 1 to 4 minute
                                       # range work well, with generation time proportional to sample length.  
                                       # This total length affects how quickly the model 
                                       # progresses through lyrics (model also generates differently
                                       # depending on if it thinks it's in the beginning, middle, or end of sample)
hps.sample_length = (int(sample_length_in_seconds*hps.sr)//top_prior.raw_to_tokens)*top_prior.raw_to_tokens
assert hps.sample_length >= top_prior.n_ctx*top_prior.raw_to_tokens, f'Please choose a larger sampling rate'


# Note: Metas can contain different prompts per sample.
# By default, all samples use the same prompt.
metas = [dict(artist = "Eminem",
            genre = "Hip Hop",
            total_length = hps.sample_length,
            offset = 0,
            lyrics = "",
            ),
          ] * hps.n_samples
labels = [None, None, top_prior.labeller.get_batch_labels(metas, 'cuda')]



sampling_temperature = .96

lower_batch_size = 16
max_batch_size = 3 if model in ('5b', '5b_lyrics') else 16
lower_level_chunk_size = 32
chunk_size = 16 if model in ('5b', '5b_lyrics') else 32
sampling_kwargs = [dict(temp=.99, fp16=True, max_batch_size=lower_batch_size,
                        chunk_size=lower_level_chunk_size),
                    dict(temp=0.99, fp16=True, max_batch_size=lower_batch_size,
                         chunk_size=lower_level_chunk_size),
                    dict(temp=sampling_temperature, fp16=True, 
                         max_batch_size=max_batch_size, chunk_size=chunk_size)]


if sample_hps.mode == 'ancestral':
  zs = [t.zeros(hps.n_samples,0,dtype=t.long, device='cuda') for _ in range(len(priors))]
  zs = _sample(zs, labels, sampling_kwargs, [None, None, top_prior], [2], hps)
elif sample_hps.mode == 'upsample':
  assert sample_hps.codes_file is not None
  # Load codes.
  data = t.load(sample_hps.codes_file, map_location='cpu')
  zs = [z.cuda() for z in data['zs']]
  assert zs[-1].shape[0] == hps.n_samples, f"Expected bs = {hps.n_samples}, got {zs[-1].shape[0]}"
  del data
  print('Falling through to the upsample step later in the notebook.')
elif sample_hps.mode == 'primed':
  assert sample_hps.audio_file is not None
  audio_files = sample_hps.audio_file.split(',')
  duration = (int(sample_hps.prompt_length_in_seconds*hps.sr)//top_prior.raw_to_tokens)*top_prior.raw_to_tokens
  x = load_prompts(audio_files, duration, hps)
  zs = top_prior.encode(x, start_level=0, end_level=len(priors), bs_chunks=x.shape[0])
  zs = _sample(zs, labels, sampling_kwargs, [None, None, top_prior], [2], hps)
else:
  raise ValueError(f'Unknown sample mode {sample_hps.mode}.')


Audio(f'{hps.name}/level_2/item_0.wav')