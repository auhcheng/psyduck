import fs from 'fs'
import path from 'path'

export function getVideoPaths() {
    const clip_dir = 'public/FinishedClips/'
    const files = fs.readdirSync(clip_dir);
    const filenames = files.map(fname => {return path.join('/FinishedClips/', fname)})
    console.log(filenames)
    return filenames
  }