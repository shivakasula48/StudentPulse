import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import {
  GitCompare,
  Target,
  Sparkles,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  ArrowRight,
  Milestone,
  FolderKanban,
  ShieldCheck,
  RefreshCw,
  AlertCircle
} from 'lucide-react';

export default function AnalysisPage() {
  const { user, refreshUser } = useAuth();
  const navigate = useNavigate();

  const [roles, setRoles] = useState([]);
  const [selectedRole, setSelectedRole] = useState(user?.target_role || 'Java Developer');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState('');

  // Fetch available roles
  useEffect(() => {
    const fetchRoles = async () => {
      try {
        const res = await api.get('/analysis/roles');
        setRoles(res.data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchRoles();
  }, []);

  // Run analysis when role changes
  const runAnalysis = async (roleName) => {
    try {
      setAnalyzing(true);
      setError('');
      const res = await api.post('/analysis/skill-gap', { target_role: roleName });
      setAnalysis(res.data);
    } catch (err) {
      console.error(err);
      setError('Failed to compute skill gap analysis.');
    } finally {
      setAnalyzing(false);
      setLoading(false);
    }
  };

  useEffect(() => {
    runAnalysis(selectedRole);
  }, [selectedRole]);

  const handleRoleChange = (e) => {
    const newRole = e.target.value;
    setSelectedRole(newRole);
  };

  const handleGenerateRoadmap = async () => {
    try {
      await api.post('/roadmap/generate', { target_role: selectedRole });
      navigate('/roadmap');
    } catch (err) {
      setError('Failed to generate roadmap.');
    }
  };

  if (loading && !analysis) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="w-10 h-10 border-4 border-cyan-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-12">
      {/* Header & Role Selector */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 rounded-3xl bg-slate-900 border border-slate-800 shadow-xl">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-950/80 border border-cyan-800/60 text-cyan-400 text-xs font-semibold mb-2">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Deterministic Matrix + AI Architectural Assessment</span>
          </div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight">
            Role-Based Skill Gap Analysis
          </h1>
          <p className="text-xs text-slate-400 mt-1 max-w-xl">
            Compares your verified assessment scores and self-reported skills against industry requirements.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <label className="text-xs font-semibold text-slate-400 uppercase whitespace-nowrap">Target Role:</label>
          <select
            value={selectedRole}
            onChange={handleRoleChange}
            className="px-4 py-2 rounded-xl bg-slate-950 border border-slate-700 text-cyan-300 font-bold text-sm outline-none focus:border-cyan-500 shadow"
          >
            <option value="Java Developer">Java Developer</option>
            <option value="Python Developer">Python Developer</option>
            <option value="Full Stack Developer">Full Stack Developer</option>
            <option value="Frontend Developer">Frontend Developer</option>
            <option value="Backend Developer">Backend Developer</option>
            <option value="Data Analyst">Data Analyst</option>
            <option value="AI/ML Engineer">AI/ML Engineer</option>
            <option value="Software Engineer">Software Engineer</option>
          </select>
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-red-950/60 border border-red-800/80 text-red-300 text-sm flex items-center gap-3">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {analysis && (
        <>
          {/* Match Metric & Explanatory Summary */}
          <div className="p-6 sm:p-8 rounded-3xl bg-slate-900 border border-slate-800 shadow-xl space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-6 pb-6 border-b border-slate-800">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
                  Role Readiness Alignment
                </span>
                <div className="text-3xl sm:text-4xl font-black text-white font-mono mt-1">
                  {analysis.match_percentage.toFixed(1)}% Match
                </div>
                <p className="text-xs text-slate-400 mt-1">
                  Evaluated against {analysis.total_required_skills} industry benchmark competencies for{' '}
                  <strong className="text-cyan-400">{analysis.target_role}</strong>.
                </p>
              </div>

              {/* Action Buttons */}
              <div className="flex flex-wrap gap-3">
                <button
                  onClick={handleGenerateRoadmap}
                  className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs shadow-lg shadow-cyan-500/20 transition"
                >
                  <Milestone className="w-4 h-4" />
                  <span>Generate Roadmap</span>
                </button>
                <button
                  onClick={() => navigate('/projects')}
                  className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs transition border border-slate-700"
                >
                  <FolderKanban className="w-4 h-4" />
                  <span>View Projects</span>
                </button>
              </div>
            </div>

            {/* AI Architectural Summary */}
            <div className="p-5 rounded-2xl bg-slate-950/70 border border-slate-800/80 space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 text-xs font-bold text-cyan-400 uppercase tracking-wider">
                  <Sparkles className="w-4 h-4" />
                  <span>Evidence-Based Career Analysis</span>
                </div>
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 font-mono">
                  {analysis.ai_is_fallback ? 'Rule-Based Engine Active' : 'Gemini 4 Analysis'}
                </span>
              </div>
              <p className="text-xs sm:text-sm text-slate-300 leading-relaxed whitespace-pre-line font-sans">
                {analysis.ai_summary}
              </p>
            </div>
          </div>

          {/* Three Categorized Skill Columns */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* 1. Strong Skills */}
            <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-5 h-5 text-teal-400" />
                  <h3 className="font-bold text-white text-base">Strong Skills</h3>
                </div>
                <span className="text-xs font-bold text-teal-400 bg-teal-950 px-2.5 py-0.5 rounded-full">
                  {analysis.strong_skills.length}
                </span>
              </div>

              {analysis.strong_skills.length > 0 ? (
                <div className="space-y-3">
                  {analysis.strong_skills.map((s, idx) => (
                    <div key={idx} className="p-3.5 rounded-xl bg-slate-950 border border-teal-900/40">
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-sm text-white">{s.skill_name}</span>
                        <span className="text-[10px] px-2 py-0.5 rounded bg-teal-950 text-teal-300 font-mono">
                          {s.current_level}
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-400 mt-1">{s.gap_reason}</p>
                      {s.assessment_score !== null && (
                        <div className="mt-2 text-[10px] text-teal-400 font-mono font-semibold">
                          Verified: {s.assessment_score.toFixed(0)}%
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-slate-500 italic py-4">No verified strong skills for this role yet.</p>
              )}
            </div>

            {/* 2. Needs Improvement */}
            <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <div className="flex items-center gap-2">
                  <AlertTriangle className="w-5 h-5 text-amber-400" />
                  <h3 className="font-bold text-white text-base">Needs Improvement</h3>
                </div>
                <span className="text-xs font-bold text-amber-400 bg-amber-950 px-2.5 py-0.5 rounded-full">
                  {analysis.needs_improvement_skills.length}
                </span>
              </div>

              {analysis.needs_improvement_skills.length > 0 ? (
                <div className="space-y-3">
                  {analysis.needs_improvement_skills.map((s, idx) => (
                    <div key={idx} className="p-3.5 rounded-xl bg-slate-950 border border-amber-900/40">
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-sm text-white">{s.skill_name}</span>
                        <span className="text-[10px] px-2 py-0.5 rounded bg-amber-950 text-amber-300 font-mono">
                          Required: {s.required_level}
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-400 mt-1">{s.gap_reason}</p>
                      <div className="mt-2 flex items-center justify-between text-[10px] text-slate-500 font-mono">
                        <span>Current: {s.current_level || 'None'}</span>
                        <span className="text-amber-400 font-bold">Priority: {s.priority}</span>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-slate-500 italic py-4">No skills currently marked for improvement.</p>
              )}
            </div>

            {/* 3. Missing Skills */}
            <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <div className="flex items-center gap-2">
                  <XCircle className="w-5 h-5 text-red-400" />
                  <h3 className="font-bold text-white text-base">Missing Skills</h3>
                </div>
                <span className="text-xs font-bold text-red-400 bg-red-950 px-2.5 py-0.5 rounded-full">
                  {analysis.missing_skills.length}
                </span>
              </div>

              {analysis.missing_skills.length > 0 ? (
                <div className="space-y-3">
                  {analysis.missing_skills.map((s, idx) => (
                    <div key={idx} className="p-3.5 rounded-xl bg-slate-950 border border-red-900/40">
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-sm text-white">{s.skill_name}</span>
                        <span className="text-[10px] px-2 py-0.5 rounded bg-red-950 text-red-300 font-mono">
                          {s.priority} Priority
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-400 mt-1">{s.gap_reason}</p>
                      <div className="mt-2 text-[10px] text-slate-500 font-mono">
                        Target: {s.required_level} Level
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-slate-500 italic py-4">Congratulations! No missing baseline skills.</p>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
