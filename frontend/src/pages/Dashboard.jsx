import React, { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import VoiceGenerator from '../components/VoiceGenerator'
import { ttsAPI } from '../api/tts'
import { CreditCard, History, Crown } from 'lucide-react'
import { Link } from 'react-router-dom'
import toast from 'react-hot-toast'

const Dashboard = () => {
  const { user } = useAuth()
  const [planInfo, setPlanInfo] = useState(null)
  const [voiceHistory, setVoiceHistory] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchPlanInfo()
    fetchVoiceHistory()
  }, [])

  const fetchPlanInfo = async () => {
    try {
      const info = await ttsAPI.getPlanInfo()
      setPlanInfo(info)
    } catch (error) {
      console.error('Failed to fetch plan info:', error)
    }
  }

  const fetchVoiceHistory = async () => {
    try {
      const history = await ttsAPI.getVoiceHistory()
      setVoiceHistory(history)
    } catch (error) {
      console.error('Failed to fetch voice history:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleGenerationComplete = () => {
    fetchPlanInfo()
    fetchVoiceHistory()
  }

  const isTrialUser = user?.plan === 'Trial'
  const canGenerate = isTrialUser ? user.daily_count < 3 : true

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600">Welcome back, {user?.name}!</p>
        </div>

        {/* Plan Status */}
        <div className="mb-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className={`p-2 rounded-full ${isTrialUser ? 'bg-yellow-100' : 'bg-green-100'}`}>
                  <Crown className={`h-6 w-6 ${isTrialUser ? 'text-yellow-600' : 'text-green-600'}`} />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    {user?.plan} Plan
                  </h3>
                  {isTrialUser && (
                    <p className="text-sm text-gray-600">
                      {3 - user.daily_count} generations remaining today
                    </p>
                  )}
                </div>
              </div>
              
              {isTrialUser && (
                <Link
                  to="/pricing"
                  className="flex items-center space-x-2 bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 transition-colors"
                >
                  <CreditCard className="h-4 w-4" />
                  <span>Upgrade Plan</span>
                </Link>
              )}
            </div>

            {planInfo && (
              <div className="mt-4">
                <h4 className="text-sm font-medium text-gray-700 mb-2">Plan Features:</h4>
                <ul className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  {planInfo.features.map((feature, index) => (
                    <li key={index} className="flex items-center text-sm text-gray-600">
                      <span className="text-green-500 mr-2">✓</span>
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>

        {/* Voice Generator */}
        <div className="mb-8">
          <VoiceGenerator 
            user={user} 
            onGenerationComplete={handleGenerationComplete}
          />
        </div>

        {/* Voice History */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center space-x-2 mb-4">
            <History className="h-5 w-5 text-gray-500" />
            <h3 className="text-lg font-semibold text-gray-900">Voice History</h3>
          </div>
          
          {loading ? (
            <div className="text-center py-4">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
            </div>
          ) : voiceHistory.length === 0 ? (
            <p className="text-gray-500 text-center py-4">No voice generations yet</p>
          ) : (
            <div className="space-y-3">
              {voiceHistory.map((entry) => (
                <div key={entry.id} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <p className="text-sm text-gray-900 mb-2">{entry.text}</p>
                      <p className="text-xs text-gray-500">
                        Generated on {new Date(entry.created_at).toLocaleString()}
                      </p>
                    </div>
                    {entry.audio_url && (
                      <audio controls className="ml-4">
                        <source src={entry.audio_url} type="audio/mpeg" />
                        Your browser does not support the audio element.
                      </audio>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Dashboard





















