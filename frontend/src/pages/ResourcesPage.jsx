import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import {
  BookOpen,
  ExternalLink,
  Search,
  Filter,
  Sparkles,
  Award,
  Code,
  GraduationCap,
  AlertCircle
} from 'lucide-react';

export default function ResourcesPage() {
  const { user } = useAuth();
  const [resources, setResources] = useState([]);
  const [recommended, setRecommended] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Filters
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedType, setSelectedType] = useState('All');

  const fetchResources = async () => {
    try {
      setLoading(true);
      const [allRes, recRes] = await Promise.all([
        api.get('/resources'),
        api.get(`/resources/recommended?target_role=${encodeURIComponent(user?.target_role || 'Java Developer')}`)
      ]);
      setResources(allRes.data);
      setRecommended(recRes.data);
    } catch (err) {
      console.error(err);
      setError('Failed to load learning resources.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchResources();
  }, [user?.target_role]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="w-10 h-10 border-4 border-cyan-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  const types = ['All', 'Documentation', 'Tutorials', 'Coding practice', 'Online courses'];

  const filteredResources = resources.filter((r) => {
    const matchesSearch = r.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          r.skill_category.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesType = selectedType === 'All' || r.resource_type.toLowerCase() === selectedType.toLowerCase();
    return matchesSearch && matchesType;
  });

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-12">
      {/* Header */}
      <div className="p-6 sm:p-8 rounded-3xl bg-slate-900 border border-slate-800 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-950/80 border border-cyan-800/60 text-cyan-400 text-xs font-semibold mb-2">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Verified Industry Learning Catalog</span>
          </div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight">
            Curated Learning Resources
          </h1>
          <p className="text-xs text-slate-400 mt-1 max-w-xl">
            Definitive official documentation, battle-tested tutorials, and interactive coding sandboxes. No dead or invented links.
          </p>
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-red-950/60 border border-red-800/80 text-red-300 text-sm flex items-center gap-3">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Recommended for Your Gaps */}
      {recommended.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-cyan-400">
            <Sparkles className="w-4 h-4" />
            <span>Recommended for Your {user?.target_role || 'Target Role'} Skill Gaps</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {recommended.slice(0, 3).map((rec) => (
              <div key={rec.id} className="p-5 rounded-2xl bg-gradient-to-b from-cyan-950/30 to-slate-900 border border-cyan-800/40 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between text-[10px] text-cyan-400 font-mono">
                    <span>{rec.skill_category}</span>
                    <span className="px-2 py-0.5 rounded bg-cyan-950 border border-cyan-800/60">{rec.resource_type}</span>
                  </div>
                  <h3 className="text-base font-bold text-white mt-2">{rec.title}</h3>
                  <p className="text-xs text-slate-300 mt-1 line-clamp-2">{rec.description}</p>
                </div>
                <a
                  href={rec.url}
                  target="_blank"
                  rel="noreferrer"
                  className="mt-4 pt-3 border-t border-cyan-950 flex items-center justify-between text-xs font-bold text-cyan-400 hover:text-cyan-300"
                >
                  <span>Open Resource</span>
                  <ExternalLink className="w-3.5 h-3.5" />
                </a>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Filter and Search Bar */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
          <input
            type="text"
            placeholder="Search by topic, library, or framework (e.g. Spring, React, Python)..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white text-xs outline-none focus:border-cyan-500 transition"
          />
        </div>

        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0">
          {types.map((t) => (
            <button
              key={t}
              onClick={() => setSelectedType(t)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition ${
                selectedType === t
                  ? 'bg-cyan-500 text-slate-950 font-bold'
                  : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
              }`}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      {/* Complete Resource Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredResources.map((res) => (
          <div
            key={res.id}
            className="p-5 rounded-2xl bg-slate-900 border border-slate-800 hover:border-slate-700 transition flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between text-[10px] text-slate-400 font-mono">
                <span className="text-cyan-400 font-bold">{res.skill_category}</span>
                <span className="px-2 py-0.5 rounded bg-slate-950 border border-slate-800">{res.resource_type}</span>
              </div>
              <h3 className="text-base font-bold text-white mt-2">{res.title}</h3>
              <p className="text-xs text-slate-400 mt-1 line-clamp-3 leading-relaxed">{res.description}</p>
            </div>

            <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
              <span className="text-[10px] text-slate-500 font-mono">Level: {res.difficulty}</span>
              <a
                href={res.url}
                target="_blank"
                rel="noreferrer"
                className="flex items-center gap-1 font-bold text-cyan-400 hover:text-cyan-300"
              >
                <span>Read Official Docs</span>
                <ExternalLink className="w-3.5 h-3.5" />
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
