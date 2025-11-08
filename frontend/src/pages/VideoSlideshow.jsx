 
import React, { useState } from 'react'
import { generateSlideshow } from '../api/video'

export default function VideoSlideshow() {
  const [files, setFiles] = useState([])
  const [duration, setDuration] = useState(2)
  const [slideEffect, setSlideEffect] = useState(true)
  const [transition, setTransition] = useState('slide')
  const [videoUrl, setVideoUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleFiles = (e) => {
    const f = Array.from(e.target.files || [])
    setFiles(f.slice(0, 3))
  }

  const onSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setVideoUrl('')
    try {
      setLoading(true)
      const res = await generateSlideshow({ files, durationSeconds: duration, slideEffect, transition })
      // Handle video URL for both local development and production
      let videoUrlToUse = res.video_url
      if (videoUrlToUse) {
        const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
        const isLocalDev = API_BASE_URL.includes('localhost:8000')
        
        // If URL contains localhost:8000 and we're in local dev, use Vite proxy
        if (videoUrlToUse.includes('localhost:8000') && isLocalDev) {
          videoUrlToUse = videoUrlToUse.replace('localhost:8000', 'localhost:3000')
        }
        // If it's a relative URL starting with /static
        else if (videoUrlToUse.startsWith('/static')) {
          // In local dev, Vite proxy will handle it
          // In production, prepend the backend URL
          if (!isLocalDev) {
            videoUrlToUse = `${API_BASE_URL}${videoUrlToUse}`
          }
        }
        // If it's not a full URL, prepend backend URL
        else if (!videoUrlToUse.startsWith('http://') && !videoUrlToUse.startsWith('https://')) {
          videoUrlToUse = `${API_BASE_URL}${videoUrlToUse}`
        }
        // If it's a full production URL, use it directly
      }
      // Cache-bust and ensure the <video> reloads with new source
      setVideoUrl(`${videoUrlToUse}?t=${Date.now()}`)
    } catch (err) {
      setError(err.message || 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-2xl font-semibold mb-4">Create Slideshow</h1>
      <form onSubmit={onSubmit} className="space-y-5 bg-white p-6 rounded-xl shadow-lg border border-gray-100">
        <div>
          <label className="block font-semibold mb-2 text-gray-800">Upload 2–3 images</label>
          <input
            type="file"
            accept="image/*"
            multiple
            onChange={handleFiles}
            className="block w-full text-sm text-gray-800 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 border rounded-md p-2"
          />
          <p className="text-sm text-gray-500 mt-2">Selected: {files.length}</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
          <div>
            <label className="block font-semibold mb-2 text-gray-800">Seconds per image</label>
            <select
              value={duration}
              onChange={(e) => setDuration(Number(e.target.value))}
              className="border rounded-md p-2 w-full bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value={2}>2</option>
              <option value={3}>3</option>
              <option value={4}>4</option>
            </select>
          </div>
          <div>
            <label className="block font-semibold mb-2 text-gray-800">Transition</label>
            <select
              value={transition}
              onChange={(e) => setTransition(e.target.value)}
              className="border rounded-md p-2 w-full bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="none">None</option>
              <option value="slide">Slide</option>
              <option value="kenburns">Ken Burns</option>
              <option value="zoom_in">Zoom In</option>
              <option value="zoom_out">Zoom Out</option>
            </select>
            <p className="text-xs text-gray-500 mt-1">Smooth motion transitions for engaging slides.</p>
          </div>
          <div className="flex items-center gap-4">
            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={slideEffect}
                onChange={(e) => setSlideEffect(e.target.checked)}
              />
              Subtle slide motion
            </label>
          </div>
        </div>

        {error && <div className="text-red-600">{error}</div>}

        <div className="flex items-center justify-between">
          <button
            type="submit"
            disabled={loading}
            className="px-5 py-2.5 bg-blue-600 text-white rounded-md disabled:opacity-60 hover:bg-blue-700 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
          >
            {loading ? 'Generating…' : 'Generate Slideshow'}
          </button>
        </div>
      </form>

      {videoUrl && (
        <div className="mt-6">
          <h2 className="text-xl font-semibold mb-2">Your Video</h2>
          <video key={videoUrl} src={videoUrl} controls className="w-full rounded shadow" />
          <div className="mt-2">
            <a href={videoUrl} download className="text-blue-600 underline">Download video</a>
          </div>
        </div>
      )}
    </div>
  )
}
