import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import {
  FolderKanban,
  Sparkles,
  Plus,
  ExternalLink,
  GitBranch,
  CheckCircle2,
  Trash2,
  AlertCircle,
  Layers,
  ChevronDown,
  ChevronUp,
  Target,
  ArrowRight,
  Code
} from 'lucide-react';

export default function ProjectsPage() {
  const { user } = useAuth();
  const [recommended, setRecommended] = useState([]);
  const [myProjects, setMyProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [expandedProj, setExpandedProj] = useState(null);

  const fetchProjectData = async () => {
    try {
      setLoading(true);
      const [recRes, myRes] = await Promise.all([
        api.get(`/projects/recommendations?target_role=${encodeURIComponent(user?.target_role || 'Java Developer')}`),
        api.get('/projects')
      ]);
      setRecommended(recRes.data);
      setMyProjects(myRes.data);
    } catch (err) {
      console.error(err);
      setError('Failed to load project hub.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProjectData();
  }, [user?.target_role]);

  const handleAdoptProject = async (proj) => {
    try {
      await api.post('/projects/adopt', {
        title: proj.title,
        description: proj.description,
        technologies: proj.technologies.join(', ')
      });
      setSuccess(`Adopted '${proj.title}' into your personal project portfolio!`);
      fetchProjectData();
      setTimeout(() => setSuccess(''), 4000);
    } catch (err) {
      setError('Failed to adopt project.');
    }
  };

  const handleUpdateStatus = async (projectId, status) => {
    try {
      await api.put(`/projects/${projectId}`, { status });
      fetchProjectData();
    } catch (err) {
      setError('Failed to update project status.');
    }
  };

  const handleDeleteProject = async (projectId) => {
    if (!window.confirm('Delete this project from your portfolio?')) return;
    try {
      await api.delete(`/projects/${projectId}`);
      fetchProjectData();
    } catch (err) {
      setError('Failed to delete project.');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="w-10 h-10 border-4 border-amber-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-12">
      {/* Header */}
      <div className="p-6 sm:p-8 rounded-3xl bg-slate-900 border border-slate-800 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-950/80 border border-amber-800/60 text-amber-400 text-xs font-semibold mb-2">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Gap-Targeting Portfolio Project Recommendations</span>
          </div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight">
            Applied Project Hub
          </h1>
          <p className="text-xs text-slate-400 mt-1 max-w-xl">
            Demonstrate your capabilities with industry-standard portfolio deliverables designed to solve actual problems for{' '}
            <strong className="text-cyan-400">{user?.target_role || 'Java Developer'}</strong>.
          </p>
        </div>
      </div>

      {success && (
        <div className="p-4 rounded-xl bg-teal-950/60 border border-teal-800/80 text-teal-300 text-sm flex items-center gap-3">
          <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
          <span>{success}</span>
        </div>
      )}

      {error && (
        <div className="p-4 rounded-xl bg-red-950/60 border border-red-800/80 text-red-300 text-sm flex items-center gap-3">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Section 1: Recommended Projects Catalog */}
      <div className="space-y-4">
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-amber-400" />
          <span>Recommended Projects Tailored to Your Skill Gaps</span>
        </h2>

        <div className="space-y-4">
          {recommended.map((proj) => {
            const isExpanded = expandedProj === proj.id;
            return (
              <div
                key={proj.id}
                className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow hover:border-slate-700 transition"
              >
                <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
                  <div className="space-y-2 flex-1">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="text-[10px] px-2.5 py-0.5 rounded-full bg-slate-950 border border-slate-800 text-amber-400 font-mono font-bold">
                        {proj.difficulty} Level
                      </span>
                      <span className="text-[10px] text-slate-400">
                        Target Skills: {proj.skills_developed.join(', ')}
                      </span>
                    </div>

                    <h3 className="text-lg font-bold text-white">{proj.title}</h3>
                    <p className="text-xs text-slate-300 leading-relaxed">{proj.description}</p>

                    <div className="flex flex-wrap gap-1.5 pt-1">
                      {proj.technologies.map((t, idx) => (
                        <span key={idx} className="text-[10px] px-2.5 py-0.5 rounded-lg bg-slate-950 border border-slate-800 text-cyan-400 font-mono">
                          {t}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="flex items-center gap-3 self-start">
                    <button
                      onClick={() => handleAdoptProject(proj)}
                      className="px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs shadow transition whitespace-nowrap"
                    >
                      + Adopt Project
                    </button>
                    <button
                      onClick={() => setExpandedProj(isExpanded ? null : proj.id)}
                      className="p-2 rounded-xl bg-slate-800 text-slate-400 hover:text-white"
                      title={isExpanded ? 'Collapse' : 'Expand Blueprint'}
                    >
                      {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                {/* Collapsible Implementation Blueprint */}
                {isExpanded && (
                  <div className="mt-6 pt-5 border-t border-slate-800 space-y-4 text-xs">
                    <div>
                      <h4 className="font-bold text-white uppercase text-[11px] tracking-wider text-slate-400">
                        Problem Statement
                      </h4>
                      <p className="mt-1 text-slate-300 leading-relaxed">{proj.problem_statement}</p>
                    </div>

                    <div>
                      <h4 className="font-bold text-white uppercase text-[11px] tracking-wider text-slate-400">
                        Core Functional Features
                      </h4>
                      <ul className="mt-1 space-y-1 list-disc list-inside text-slate-300">
                        {proj.features.map((feat, i) => (
                          <li key={i}>{feat}</li>
                        ))}
                      </ul>
                    </div>

                    <div>
                      <h4 className="font-bold text-white uppercase text-[11px] tracking-wider text-slate-400">
                        Suggested Implementation Milestones
                      </h4>
                      <div className="mt-2 space-y-1.5">
                        {proj.implementation_steps.map((step, i) => (
                          <div key={i} className="p-2 rounded-lg bg-slate-950 text-slate-300 border border-slate-800/80 font-mono text-[11px]">
                            {step}
                          </div>
                        ))}
                      </div>
                    </div>

                    <div>
                      <h4 className="font-bold text-white uppercase text-[11px] tracking-wider text-slate-400">
                        Expected Deliverable Outcome
                      </h4>
                      <p className="mt-1 text-teal-400 font-medium">{proj.expected_outcome}</p>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Section 2: Personal Adopted Projects Portfolio */}
      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow space-y-4">
        <h2 className="text-lg font-bold text-white">Your Active Portfolio Projects</h2>

        {myProjects.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {myProjects.map((p) => (
              <div key={p.id} className="p-5 rounded-xl bg-slate-950 border border-slate-800/80 flex flex-col justify-between">
                <div>
                  <div className="flex items-start justify-between gap-2">
                    <h3 className="font-bold text-white text-base">{p.title}</h3>
                    <select
                      value={p.status}
                      onChange={(e) => handleUpdateStatus(p.id, e.target.value)}
                      className="px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-700 text-xs font-semibold text-cyan-300"
                    >
                      <option value="Planned">Planned</option>
                      <option value="In Progress">In Progress</option>
                      <option value="Completed">Completed</option>
                    </select>
                  </div>

                  <p className="text-xs text-slate-400 mt-2 line-clamp-2">{p.description}</p>
                  {p.technologies && (
                    <div className="mt-3 flex flex-wrap gap-1">
                      {p.technologies.split(',').map((tech, idx) => (
                        <span key={idx} className="text-[10px] px-2 py-0.5 rounded bg-slate-900 border border-slate-700/60 text-slate-300 font-mono">
                          {tech.trim()}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between text-xs">
                  <div className="flex items-center gap-3">
                    {p.github_url && (
                      <a href={p.github_url} target="_blank" rel="noreferrer" className="flex items-center gap-1 text-slate-400 hover:text-white">
                        <GitBranch className="w-3.5 h-3.5" />
                        <span>Code</span>
                      </a>
                    )}
                    {p.live_url && (
                      <a href={p.live_url} target="_blank" rel="noreferrer" className="flex items-center gap-1 text-cyan-400 hover:text-cyan-300">
                        <ExternalLink className="w-3.5 h-3.5" />
                        <span>Live</span>
                      </a>
                    )}
                  </div>

                  <button
                    onClick={() => handleDeleteProject(p.id)}
                    className="text-slate-500 hover:text-red-400 p-1"
                    title="Remove Project"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-slate-500 italic py-4">No active projects yet. Adopt a recommendation above!</p>
        )}
      </div>
    </div>
  );
}
