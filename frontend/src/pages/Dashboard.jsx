import React, { useState, useEffect } from 'react'
import {
  LayoutDashboard,
  Search,
  MessageSquare,
  Clock,
  ChevronDown,
  ChevronUp,
  Loader2,
  AlertCircle,
  Activity,
  CalendarDays,
} from 'lucide-react'
import api from '../services/api'

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  })
}

const formatTime = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleTimeString('fr-FR', {
    hour: '2-digit',
    minute: '2-digit',
  })
}

const StatCard = ({ icon: Icon, label, value, color }) => (
  <div className="bg-white rounded-xl border border-gray-200 p-5">
    <div className="flex items-center gap-3">
      <div className={`flex items-center justify-center w-10 h-10 rounded-lg ${color}`}>
        <Icon className="w-5 h-5" />
      </div>
      <div>
        <p className="text-2xl font-bold text-gray-900">{value}</p>
        <p className="text-xs text-gray-500">{label}</p>
      </div>
    </div>
  </div>
)

const QueryCard = ({ query }) => {
  const [expanded, setExpanded] = useState(false)

  return (
    <div className="bg-white rounded-xl border border-gray-200 hover:border-gray-300 transition">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-start gap-4 p-4 text-left cursor-pointer"
      >
        <div className="flex items-center justify-center w-8 h-8 bg-sky-100 rounded-lg shrink-0 mt-0.5">
          <MessageSquare className="w-4 h-4 text-sky-600" />
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium text-gray-900 truncate pr-4">
            {query.question}
          </p>
          <div className="flex items-center gap-3 mt-1">
            <span className="flex items-center gap-1 text-xs text-gray-400">
              <CalendarDays className="w-3 h-3" />
              {formatDate(query.created_at)}
            </span>
            <span className="flex items-center gap-1 text-xs text-gray-400">
              <Clock className="w-3 h-3" />
              {formatTime(query.created_at)}
            </span>
          </div>
        </div>
        <div className="shrink-0 mt-1">
          {expanded ? (
            <ChevronUp className="w-4 h-4 text-gray-400" />
          ) : (
            <ChevronDown className="w-4 h-4 text-gray-400" />
          )}
        </div>
      </button>

      {expanded && (
        <div className="px-4 pb-4 pt-0 ml-12 border-t border-gray-100 mt-0">
          <div className="pt-3">
            <p className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-2">
              Réponse
            </p>
            <div className="text-sm text-gray-700 leading-relaxed bg-gray-50 rounded-lg p-3 whitespace-pre-wrap">
              {query.response}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

const Dashboard = () => {
  const [queries, setQueries] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetchHistory()
  }, [])

  const fetchHistory = async () => {
    try {
      setLoading(true)
      const response = await api.get('/query/historiques')
      setQueries(response.data)
    } catch (err) {
      setError('Impossible de charger l\'historique.')
    } finally {
      setLoading(false)
    }
  }

  const filteredQueries = queries.filter(
    (q) =>
      q.question.toLowerCase().includes(searchTerm.toLowerCase()) ||
      q.response.toLowerCase().includes(searchTerm.toLowerCase())
  )

  // Stats
  const totalQueries = queries.length
  const todayQueries = queries.filter((q) => {
    const today = new Date().toDateString()
    return new Date(q.created_at).toDateString() === today
  }).length
  const thisWeekQueries = queries.filter((q) => {
    const now = new Date()
    const weekAgo = new Date(now.getFullYear(), now.getMonth(), now.getDate() - 7)
    return new Date(q.created_at) >= weekAgo
  }).length

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="flex flex-col items-center gap-3">
          <Loader2 className="w-8 h-8 text-sky-600 animate-spin" />
          <p className="text-sm text-gray-500">Chargement de l'historique...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="flex flex-col items-center gap-3 text-center">
          <div className="flex items-center justify-center w-12 h-12 bg-red-100 rounded-xl">
            <AlertCircle className="w-6 h-6 text-red-600" />
          </div>
          <p className="text-sm text-gray-600">{error}</p>
          <button
            onClick={fetchHistory}
            className="px-4 py-2 text-sm bg-sky-600 text-white rounded-lg hover:bg-sky-700 transition cursor-pointer"
          >
            Réessayer
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="h-full overflow-y-auto">
      <div className="max-w-5xl mx-auto px-6 py-6 space-y-6">
        {/* Header */}
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center w-9 h-9 bg-sky-100 rounded-lg">
            <LayoutDashboard className="w-5 h-5 text-sky-600" />
          </div>
          <div>
            <h1 className="text-lg font-semibold text-gray-900">Dashboard</h1>
            <p className="text-xs text-gray-500">
              Historique de vos interactions
            </p>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <StatCard
            icon={MessageSquare}
            label="Total requêtes"
            value={totalQueries}
            color="bg-sky-100 text-sky-600"
          />
          <StatCard
            icon={Activity}
            label="Cette semaine"
            value={thisWeekQueries}
            color="bg-emerald-100 text-emerald-600"
          />
          <StatCard
            icon={Clock}
            label="Aujourd'hui"
            value={todayQueries}
            color="bg-amber-100 text-amber-600"
          />
        </div>

        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Rechercher dans l'historique..."
            className="w-full pl-10 pr-4 py-2.5 bg-white border border-gray-200 rounded-xl text-sm text-gray-900 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-transparent transition"
          />
        </div>

        {/* History list */}
        <div className="space-y-3">
          {filteredQueries.length === 0 ? (
            <div className="flex flex-col items-center py-12 text-center">
              <MessageSquare className="w-10 h-10 text-gray-300 mb-3" />
              <p className="text-sm text-gray-500">
                {searchTerm
                  ? 'Aucun résultat trouvé.'
                  : 'Aucune interaction pour le moment.'}
              </p>
              {searchTerm && (
                <button
                  onClick={() => setSearchTerm('')}
                  className="mt-2 text-sm text-sky-600 hover:underline cursor-pointer"
                >
                  Effacer la recherche
                </button>
              )}
            </div>
          ) : (
            filteredQueries
              .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
              .map((query) => <QueryCard key={query.id} query={query} />)
          )}
        </div>
      </div>
    </div>
  )
}

export default Dashboard
