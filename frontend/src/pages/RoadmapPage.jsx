import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import {
  Milestone,
  CheckCircle2,
  Clock,
  ExternalLink,
  Target,
  Sparkles,
  BookOpen,
  Calendar,
  AlertCircle,
  RefreshCw,
  Flame,
  Check
} from 'lucide-react';

export default function RoadmapPage() {
  const { user } = useAuth();
  const [roadmap, setRoadmap] = useState(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState('');
  const [filterPhase, setFilterPhase] = useState('All');

  const fetchRoadmap = async () => {
    try {
      setLoading(true);
      const res = await api.get('/roadmap');
      setRoadmap(res.data);
    } catch (err) {
      console.error(err);
      setError('Failed to load learning roadmap.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRoadmap();
  }, []);

  const handleGenerateRoadmap = async () => {
    try {
      setGenerating(true);
      setError('');
      const res = await api.post('/roadmap/generate', {
        target_role: user?.target_role || 'Java Developer'
      });
      setRoadmap(res.data);
    } catch (err) {
      setError('Failed to regenerate roadmap.');
    } finally {
      setGenerating(false);
    }
  };

  const handleUpdateTaskStatus = async (taskId, newStatus) => {
    try {
      await api.put(`/roadmap/tasks/${taskId}`, { status: newStatus });
      fetchRoadmap();
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="w-10 h-10 border-4 border-teal-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  const tasks = roadmap?.tasks || [];
  const completedTasks = tasks.filter((t) => t.status === 'Completed').length;
  const progressPct = tasks.length > 0 ? Math.round((completedTasks / tasks.length) * 100) : 0;

  // Extract unique phases
  const phases = ['All', ...new Set(tasks.map((t) => t.phase))];

  const filteredTasks = tasks.filter((t) => {
    if (filterPhase === 'All') return true;
    return t.phase === filterPhase;
  });

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-12">
      {/* Top Banner */}
      <div className="p-6 sm:p-8 rounded-3xl bg-slate-900 border border-slate-800 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-950/80 border border-teal-800/60 text-teal-400 text-xs font-semibold mb-2">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Personalized Action & Skill Acceleration Plan</span>
          </div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight">
            {roadmap?.title || 'Personalized Learning Roadmap'}
          </h1>
          <p className="text-xs text-slate-400 mt-1 max-w-xl">
            Custom-built phased curriculum tailored to address your specific skill gaps for{' '}
            <strong className="text-cyan-400">{roadmap?.target_role || 'your career goal'}</strong>.
          </p>
        </div>

        <button
          onClick={handleGenerateRoadmap}
          disabled={generating}
          className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-teal-500 hover:bg-teal-400 text-slate-950 font-bold text-xs shadow-lg transition self-start md:self-auto disabled:opacity-50"
        >
          <RefreshCw className={`w-4 h-4 ${generating ? 'animate-spin' : ''}`} />
          <span>{generating ? 'Regenerating...' : 'Re-sync with Current Gaps'}</span>
        </button>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-red-950/60 border border-red-800/80 text-red-300 text-sm flex items-center gap-3">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Progress & Milestone Overview */}
      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Roadmap Completion</span>
            <div className="text-2xl font-black text-white font-mono mt-0.5">
              {progressPct}% ({completedTasks}/{tasks.length} Tasks Done)
            </div>
          </div>

          {/* Phase Filter Tabs */}
          <div className="flex items-center gap-2 overflow-x-auto pb-1 sm:pb-0">
            {phases.map((ph) => (
              <button
                key={ph}
                onClick={() => setFilterPhase(ph)}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition ${
                  filterPhase === ph
                    ? 'bg-teal-500 text-slate-950 font-bold'
                    : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
                }`}
              >
                {ph}
              </button>
            ))}
          </div>
        </div>

        {/* Progress Bar */}
        <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
          <div
            className="bg-teal-400 h-full rounded-full transition-all duration-500"
            style={{ width: `${progressPct}%` }}
          ></div>
        </div>
      </div>

      {/* Phased Tasks List */}
      <div className="space-y-4">
        {filteredTasks.length > 0 ? (
          filteredTasks.map((t) => (
            <div
              key={t.id}
              className={`p-6 rounded-2xl bg-slate-900 border transition ${
                t.status === 'Completed'
                  ? 'border-teal-900/60 bg-slate-900/40 opacity-80'
                  : t.status === 'In Progress'
                  ? 'border-cyan-500/50 shadow-md'
                  : 'border-slate-800'
              }`}
            >
              <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
                <div className="space-y-2 flex-1">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="text-[10px] px-2.5 py-0.5 rounded-full bg-slate-950 border border-slate-800 text-teal-400 font-mono font-semibold">
                      {t.phase}
                    </span>
                    <span
                      className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase ${
                        t.priority === 'Critical'
                          ? 'bg-red-950 text-red-400 border border-red-800/60'
                          : t.priority === 'High'
                          ? 'bg-amber-950 text-amber-400 border border-amber-800/60'
                          : 'bg-slate-800 text-slate-300'
                      }`}
                    >
                      {t.priority} Priority
                    </span>
                    <span className="text-[10px] text-slate-400 font-mono">
                      ⏱ Duration: {t.estimated_duration}
                    </span>
                  </div>

                  <h3 className={`text-base font-bold ${t.status === 'Completed' ? 'line-through text-slate-400' : 'text-white'}`}>
                    {t.title}
                  </h3>

                  <p className="text-xs text-slate-400 leading-relaxed">{t.description}</p>

                  {t.learning_objective && (
                    <div className="text-[11px] text-slate-300 bg-slate-950/70 p-3 rounded-xl border border-slate-800/80">
                      <strong className="text-teal-400">Objective:</strong> {t.learning_objective}
                    </div>
                  )}

                  {t.recommended_resources && (
                    <div className="flex items-center gap-1.5 text-xs text-cyan-400 pt-1">
                      <BookOpen className="w-3.5 h-3.5" />
                      <span>Resources: {t.recommended_resources}</span>
                    </div>
                  )}
                </div>

                {/* Status Switcher Controls */}
                <div className="flex sm:flex-col items-center gap-2 self-start">
                  <select
                    value={t.status}
                    onChange={(e) => handleUpdateTaskStatus(t.id, e.target.value)}
                    className={`px-3 py-1.5 rounded-xl text-xs font-bold outline-none border transition ${
                      t.status === 'Completed'
                        ? 'bg-teal-950/80 border-teal-700 text-teal-300'
                        : t.status === 'In Progress'
                        ? 'bg-cyan-950/80 border-cyan-700 text-cyan-300'
                        : 'bg-slate-950 border-slate-700 text-slate-300'
                    }`}
                  >
                    <option value="Pending">Pending</option>
                    <option value="In Progress">In Progress</option>
                    <option value="Completed">Completed</option>
                  </select>

                  {t.status !== 'Completed' && (
                    <button
                      onClick={() => handleUpdateTaskStatus(t.id, 'Completed')}
                      className="p-1.5 rounded-lg bg-teal-500/10 hover:bg-teal-500/20 text-teal-400 text-[10px] font-semibold flex items-center gap-1"
                      title="Quick Mark Done"
                    >
                      <Check className="w-3.5 h-3.5" />
                      <span className="hidden sm:inline">Done</span>
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="p-12 rounded-2xl bg-slate-900 border border-dashed border-slate-800 text-center">
            <Milestone className="w-10 h-10 text-slate-600 mx-auto mb-3" />
            <p className="text-xs text-slate-400">No tasks in this phase.</p>
          </div>
        )}
      </div>
    </div>
  );
}
