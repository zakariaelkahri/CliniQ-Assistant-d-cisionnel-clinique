import React, { useState, useRef, useEffect } from 'react'
import { Send, Bot, User, Loader2, Sparkles } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import api from '../services/api'

const TypingIndicator = () => (
  <div className="flex items-start gap-3 animate-fade-in-up">
    <div className="flex items-center justify-center w-8 h-8 bg-sky-100 rounded-lg shrink-0">
      <Bot className="w-4 h-4 text-sky-600" />
    </div>
    <div className="bg-white border border-gray-200 rounded-2xl rounded-tl-sm px-4 py-3">
      <div className="flex gap-1.5">
        <span className="typing-dot w-2 h-2 bg-gray-400 rounded-full inline-block" />
        <span className="typing-dot w-2 h-2 bg-gray-400 rounded-full inline-block" />
        <span className="typing-dot w-2 h-2 bg-gray-400 rounded-full inline-block" />
      </div>
    </div>
  </div>
)

const ChatMessage = ({ message }) => {
  const isUser = message.role === 'user'

  return (
    <div
      className={`flex items-start gap-3 animate-fade-in-up ${
        isUser ? 'flex-row-reverse' : ''
      }`}
    >
      <div
        className={`flex items-center justify-center w-8 h-8 rounded-lg shrink-0 ${
          isUser ? 'bg-sky-600' : 'bg-sky-100'
        }`}
      >
        {isUser ? (
          <User className="w-4 h-4 text-white" />
        ) : (
          <Bot className="w-4 h-4 text-sky-600" />
        )}
      </div>
      <div
        className={`max-w-[75%] px-4 py-3 text-sm leading-relaxed ${
          isUser
            ? 'bg-sky-600 text-white rounded-2xl rounded-tr-sm'
            : 'bg-white border border-gray-200 text-gray-800 rounded-2xl rounded-tl-sm'
        }`}
      >
        {isUser ? (
          <p>{message.content}</p>
        ) : (
          <div className="markdown-content">
            <ReactMarkdown>{message.content}</ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  )
}

const Assistant = () => {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, loading])

  const handleSubmit = async (e) => {
    e.preventDefault()
    const question = input.trim()
    if (!question || loading) return

    const userMessage = { role: 'user', content: question }
    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await api.post('/query/assistant', { question })
      const botMessage = {
        role: 'assistant',
        content: response.data.answer,
      }
      setMessages((prev) => [...prev, botMessage])
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content:
            "Désolé, une erreur s'est produite. Veuillez réessayer.",
        },
      ])
    } finally {
      setLoading(false)
      inputRef.current?.focus()
    }
  }

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center gap-3 px-6 py-4 bg-white border-b border-gray-200">
        <div className="flex items-center justify-center w-9 h-9 bg-sky-100 rounded-lg">
          <Sparkles className="w-5 h-5 text-sky-600" />
        </div>
        <div>
          <h2 className="text-sm font-semibold text-gray-900">
            Assistant Médical
          </h2>
          <p className="text-xs text-gray-500">
            Posez vos questions cliniques
          </p>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-6 space-y-4 bg-gray-50/50">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <div className="flex items-center justify-center w-16 h-16 bg-sky-100 rounded-2xl mb-4">
              <Bot className="w-8 h-8 text-sky-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-1">
              Bienvenue sur CliniQ
            </h3>
            <p className="text-sm text-gray-500 max-w-sm">
              Posez une question sur les protocoles médicaux et je vous
              fournirai une réponse basée sur les guides cliniques.
            </p>
            <div className="flex flex-wrap gap-2 mt-6 max-w-md justify-center">
              {[
                'Quel est le protocole pour une hypertension ?',
                'Comment traiter une infection urinaire ?',
                'Conduite à tenir devant une douleur thoracique ?',
              ].map((suggestion) => (
                <button
                  key={suggestion}
                  onClick={() => setInput(suggestion)}
                  className="px-3 py-2 text-xs text-sky-700 bg-sky-50 border border-sky-200 rounded-lg hover:bg-sky-100 transition cursor-pointer"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg, i) => (
          <ChatMessage key={i} message={msg} />
        ))}

        {loading && <TypingIndicator />}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="px-6 py-4 bg-white border-t border-gray-200">
        <form onSubmit={handleSubmit} className="flex items-center gap-3">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Posez votre question médicale..."
            disabled={loading}
            className="flex-1 px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm text-gray-900 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-transparent transition disabled:opacity-60"
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="flex items-center justify-center w-10 h-10 bg-sky-600 hover:bg-sky-700 disabled:bg-gray-300 text-white rounded-xl transition cursor-pointer disabled:cursor-not-allowed"
          >
            {loading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </button>
        </form>
      </div>
    </div>
  )
}

export default Assistant