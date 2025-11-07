import React from 'react'
import { Link } from 'react-router-dom'
import { Mic, Zap, Shield, ArrowRight } from 'lucide-react'

const Landing = () => {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-primary-600 to-primary-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Transform Text into
              <span className="block text-yellow-300">Natural Speech</span>
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-primary-100">
              Create high-quality AI voices with our advanced text-to-speech technology
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/register"
                className="bg-yellow-400 text-primary-900 px-8 py-3 rounded-lg text-lg font-semibold hover:bg-yellow-300 transition-colors"
              >
                Start Free Trial
              </Link>
              <Link
                to="/pricing"
                className="border-2 border-white text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-white hover:text-primary-600 transition-colors"
              >
                View Pricing
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Why Choose MyAIStudio?
            </h2>
            <p className="text-xl text-gray-600">
              Powerful features for all your voice generation needs
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Mic className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                High-Quality Voices
              </h3>
              <p className="text-gray-600">
                Generate natural-sounding voices with our advanced AI technology
              </p>
            </div>

            <div className="text-center">
              <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Zap className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Fast Generation
              </h3>
              <p className="text-gray-600">
                Get your voice files in seconds with our optimized processing
              </p>
            </div>

            <div className="text-center">
              <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Shield className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Secure & Private
              </h3>
              <p className="text-gray-600">
                Your data is protected with enterprise-grade security
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Preview */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Simple, Transparent Pricing
            </h2>
            <p className="text-xl text-gray-600">
              Choose the plan that fits your needs
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {/* Trial Plan */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Free Trial</h3>
              <div className="text-3xl font-bold text-gray-900 mb-4">$0</div>
              <ul className="space-y-2 mb-6">
                <li className="flex items-center text-gray-600">
                  <span className="text-green-500 mr-2">✓</span>
                  3 generations per day
                </li>
                <li className="flex items-center text-gray-600">
                  <span className="text-green-500 mr-2">✓</span>
                  Watermarked audio
                </li>
                <li className="flex items-center text-gray-600">
                  <span className="text-green-500 mr-2">✓</span>
                  Basic quality
                </li>
              </ul>
              <Link
                to="/register"
                className="w-full bg-gray-600 text-white py-2 px-4 rounded-md hover:bg-gray-700 transition-colors text-center block"
              >
                Start Free Trial
              </Link>
            </div>

            {/* Starter Plan */}
            <div className="bg-white rounded-lg shadow-md p-6 border-2 border-primary-500 relative">
              <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                <span className="bg-primary-500 text-white px-3 py-1 rounded-full text-sm font-semibold">
                  Most Popular
                </span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Starter</h3>
              <div className="text-3xl font-bold text-gray-900 mb-4">₨500<span className="text-lg text-gray-500">/month</span></div>
              <ul className="space-y-2 mb-6">
                <li className="flex items-center text-gray-600">
                  <span className="text-green-500 mr-2">✓</span>
                  Unlimited generations
                </li>
                <li className="flex items-center text-gray-600">
                  <span className="text-green-500 mr-2">✓</span>
                  High-quality audio
                </li>
                <li className="flex items-center text-gray-600">
                  <span className="text-green-500 mr-2">✓</span>
                  Download enabled
                </li>
                <li className="flex items-center text-gray-600">
                  <span className="text-green-500 mr-2">✓</span>
                  No watermarks
                </li>
              </ul>
              <Link
                to="/pricing"
                className="w-full bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 transition-colors text-center block"
              >
                Choose Starter
              </Link>
            </div>

            {/* Pro Plan */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Pro</h3>
              <div className="text-3xl font-bold text-gray-900 mb-4">₨1000<span className="text-lg text-gray-500">/month</span></div>
              <ul className="space-y-2 mb-6">
                <li className="flex items-center text-gray-600">
                  <span className="text-green-500 mr-2">✓</span>
                  Everything in Starter
                </li>
                <li className="flex items-center text-gray-600">
                  <span className="text-green-500 mr-2">✓</span>
                  Premium quality
                </li>
                <li className="flex items-center text-gray-600">
                  <span className="text-green-500 mr-2">✓</span>
                  Priority processing
                </li>
                <li className="flex items-center text-gray-600">
                  <span className="text-green-500 mr-2">✓</span>
                  Advanced features
                </li>
              </ul>
              <Link
                to="/pricing"
                className="w-full bg-gray-600 text-white py-2 px-4 rounded-md hover:bg-gray-700 transition-colors text-center block"
              >
                Choose Pro
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-primary-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Ready to Get Started?
          </h2>
          <p className="text-xl mb-8 text-primary-100">
            Join thousands of users creating amazing voice content
          </p>
          <Link
            to="/register"
            className="inline-flex items-center space-x-2 bg-yellow-400 text-primary-900 px-8 py-3 rounded-lg text-lg font-semibold hover:bg-yellow-300 transition-colors"
          >
            <span>Start Your Free Trial</span>
            <ArrowRight className="h-5 w-5" />
          </Link>
        </div>
      </section>
    </div>
  )
}

export default Landing





















