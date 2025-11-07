import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { Check, X } from 'lucide-react'
import { paymentAPI } from '../api/payment'
import toast from 'react-hot-toast'

const Pricing = () => {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [loading, setLoading] = useState(null)

  const plans = [
    {
      name: 'Free Trial',
      price: 0,
      currency: 'PKR',
      period: '',
      description: 'Perfect for trying out our service',
      features: [
        '3 voice generations per day',
        'Watermarked audio',
        'Basic quality',
        'No download option'
      ],
      limitations: [
        'Limited to 3 generations daily',
        'Audio includes watermark',
        'Cannot download files'
      ],
      buttonText: 'Current Plan',
      buttonDisabled: true,
      popular: false
    },
    {
      name: 'Starter',
      price: 500,
      currency: 'PKR',
      period: '/month',
      description: 'Great for personal use',
      features: [
        'Unlimited voice generations',
        'High-quality audio',
        'Download enabled',
        'No watermarks',
        'Fast processing'
      ],
      limitations: [],
      buttonText: 'Choose Starter',
      buttonDisabled: false,
      popular: true
    },
    {
      name: 'Pro',
      price: 1000,
      currency: 'PKR',
      period: '/month',
      description: 'Perfect for professionals',
      features: [
        'Everything in Starter',
        'Premium quality voices',
        'Priority processing',
        'Advanced voice options',
        'API access',
        'Priority support'
      ],
      limitations: [],
      buttonText: 'Choose Pro',
      buttonDisabled: false,
      popular: false
    }
  ]

  const handleUpgrade = async (planName) => {
    if (!user) {
      navigate('/login')
      return
    }

    if (user.plan === planName) {
      toast.error('You are already on this plan')
      return
    }

    setLoading(planName)
    try {
      const result = await paymentAPI.triggerUpgrade(planName)
      if (result.success) {
        // Redirect to payment URL
        window.location.href = result.payment_url
      } else {
        toast.error(result.error || 'Failed to initiate payment')
      }
    } catch (error) {
      console.error('Payment error:', error)
      toast.error('Failed to initiate payment. Please try again.')
    } finally {
      setLoading(null)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Choose Your Plan
          </h1>
          <p className="text-xl text-gray-600">
            Select the perfect plan for your voice generation needs
          </p>
        </div>

        {/* Pricing Cards */}
        <div className="grid md:grid-cols-3 gap-8">
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={`bg-white rounded-lg shadow-lg p-6 relative ${
                plan.popular ? 'border-2 border-primary-500' : 'border border-gray-200'
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                  <span className="bg-primary-500 text-white px-3 py-1 rounded-full text-sm font-semibold">
                    Most Popular
                  </span>
                </div>
              )}

              <div className="text-center mb-6">
                <h3 className="text-2xl font-bold text-gray-900 mb-2">{plan.name}</h3>
                <div className="mb-2">
                  <span className="text-4xl font-bold text-gray-900">
                    {plan.currency}{plan.price}
                  </span>
                  <span className="text-gray-500">{plan.period}</span>
                </div>
                <p className="text-gray-600">{plan.description}</p>
              </div>

              {/* Features */}
              <div className="mb-6">
                <h4 className="text-sm font-semibold text-gray-900 mb-3">Features:</h4>
                <ul className="space-y-2">
                  {plan.features.map((feature, index) => (
                    <li key={index} className="flex items-center text-sm text-gray-600">
                      <Check className="h-4 w-4 text-green-500 mr-2 flex-shrink-0" />
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Limitations */}
              {plan.limitations.length > 0 && (
                <div className="mb-6">
                  <h4 className="text-sm font-semibold text-gray-900 mb-3">Limitations:</h4>
                  <ul className="space-y-2">
                    {plan.limitations.map((limitation, index) => (
                      <li key={index} className="flex items-center text-sm text-gray-500">
                        <X className="h-4 w-4 text-red-500 mr-2 flex-shrink-0" />
                        {limitation}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Button */}
              <button
                onClick={() => handleUpgrade(plan.name)}
                disabled={plan.buttonDisabled || loading === plan.name}
                className={`w-full py-2 px-4 rounded-md font-medium transition-colors ${
                  plan.buttonDisabled
                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    : plan.popular
                    ? 'bg-primary-600 text-white hover:bg-primary-700'
                    : 'bg-gray-600 text-white hover:bg-gray-700'
                }`}
              >
                {loading === plan.name ? 'Processing...' : plan.buttonText}
              </button>
            </div>
          ))}
        </div>

        {/* FAQ Section */}
        <div className="mt-16">
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-8">
            Frequently Asked Questions
          </h2>
          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                How does the free trial work?
              </h3>
              <p className="text-gray-600">
                The free trial gives you 3 voice generations per day with watermarked audio. 
                Perfect for testing our service before upgrading.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Can I cancel anytime?
              </h3>
              <p className="text-gray-600">
                Yes, you can cancel your subscription at any time. You'll continue to have 
                access until the end of your current billing period.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                What payment methods do you accept?
              </h3>
              <p className="text-gray-600">
                We accept payments through Easypaisa, making it easy for Pakistani users 
                to upgrade their plans securely.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Is there a difference in voice quality?
              </h3>
              <p className="text-gray-600">
                Yes, Pro plan users get access to premium voice models with higher quality 
                and more natural-sounding voices.
              </p>
            </div>
          </div>
        </div>

        {/* CTA */}
        <div className="mt-16 text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Ready to get started?
          </h2>
          <p className="text-gray-600 mb-6">
            Join thousands of users creating amazing voice content
          </p>
          {!user ? (
            <Link
              to="/register"
              className="bg-primary-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-primary-700 transition-colors"
            >
              Start Free Trial
            </Link>
          ) : (
            <Link
              to="/dashboard"
              className="bg-primary-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-primary-700 transition-colors"
            >
              Go to Dashboard
            </Link>
          )}
        </div>
      </div>
    </div>
  )
}

export default Pricing





















