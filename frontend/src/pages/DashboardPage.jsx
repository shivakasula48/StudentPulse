import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import {
  TrendingUp,
  Award,
  CheckCircle2,
  Milestone,
  FolderKanban,
  Target,
  ArrowRight,
  Sparkles,
  Clock,
  AlertCircle,
  Activity,
  Layers,
  ChevronRight,
  UserCheck
} from 'lucide-react';
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell
} from 'recharts';

export default function DashboardPage() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchDashboard = async () => {
    try {
      setLoading(true);
      const res = await api.get('/dashboard/summary');
      setSummary(res.data);
    } catch (err) {
      console.error('Failed to load dashboard summary:', err);
      setError('Unable to load career readiness metrics.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboard();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-cyan-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-sm text-slate-400 font-medium">Computing genuine career readiness metrics...</p>
        </div>
      </div>
    );
  }

  if (error || !summary) {
    return (
      <div className="p-8 rounded-2xl bg-red-950/40 border border-red-800/60 text-red-300 flex items-center gap-4">
        <AlertCircle className="w-6 h-6 flex-shrink-0" />
        <div>
          <h3 className="font-bold text-lg">Failed to Load Dashboard</h3>
          <p className="text-sm mt-1">{error || 'Please check your connection and try again.'}</p>
          <button
            onClick={fetchDashboard}
            className="mt-3 px-4 py-1.5 rounded-lg bg-red-900/60 hover:bg-red-800 text-xs font-semibold"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  // Format Radar data
  const radarData = summary.category_proficiency || [];

  // Bar chart data for skill gap breakdown
  const gapChartData = [
    { name: 'Strong Skills', count: summary.skill_gap_summary.strong, fill: '#14b8a6' },
    { name: 'Needs Improvement', count: summary.skill_gap_summary.needs_improvement, fill: '#f59e0b' },
    { name: 'Missing Skills', count: summary.skill_gap_summary.missing, fill: '#ef4444' }
  ];

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-12">
      {/* Welcome Banner */}
      <div className="p-6 sm:p-8 rounded-3xl bg-gradient-to-r from-slate-900 via-slate-900 to-indigo-950/70 border border-slate-800 relative overflow-hidden shadow-xl">
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-950/80 border border-cyan-800/60 text-cyan-400 text-xs font-semibold mb-3">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Evidence-Backed Success Platform</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              Welcome back, {summary.user_name}
            </h1>
            <p className="mt-1 text-sm text-slate-300 max-w-2xl leading-relaxed">
              Target Career Role:{' '}
              <span className="text-cyan-400 font-bold">{summary.target_role}</span>. Here is your evidence-based readiness evaluation.
            </p>
          </div>

          {/* Holistic Readiness Score Gauge */}
          <div className="flex-shrink-0 flex items-center gap-4 p-4 rounded-2xl bg-slate-950/80 border border-slate-800/80 shadow-inner">
            <div className="relative w-20 h-20 flex items-center justify-center">
              <svg className="w-20 h-20 transform -rotate-90">
                <circle
                  cx="40"
                  cy="40"
                  r="34"
                  stroke="#1e293b"
                  strokeWidth="6"
                  fill="transparent"
                />
                <circle
                  cx="40"
                  cy="40"
                  r="34"
                  stroke={summary.readiness_score > 70 ? '#14b8a6' : (summary.readiness_score > 40 ? '#0284c7' : '#f59e0b')}
                  strokeWidth="6"
                  strokeDasharray={2 * Math.PI * 34}
                  strokeDashoffset={2 * Math.PI * 34 * (1 - summary.readiness_score / 100)}
                  strokeLinecap="round"
                  fill="transparent"
                  className="transition-all duration-1000 ease-out"
                />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
                <span className="text-xl font-extrabold text-white font-mono">{summary.readiness_score}%</span>
              </div>
            </div>
            <div>
              <div className="text-[11px] uppercase tracking-wider text-slate-400 font-bold">Career Readiness</div>
              <div className="text-xs text-cyan-400 font-semibold mt-0.5">
                {summary.readiness_score >= 75 ? 'Industry Ready' : summary.readiness_score >= 50 ? 'Progressing Well' : 'Early Phase'}
              </div>
              <div className="text-[10px] text-slate-400 mt-1">Calculated from genuine records</div>
            </div>
          </div>
        </div>
      </div>

      {/* Recommended Next Action Card */}
      {summary.recommended_next_action && (
        <div className="p-5 sm:p-6 rounded-2xl bg-gradient-to-r from-cyan-950/40 via-slate-900 to-indigo-950/40 border border-cyan-800/40 flex flex-col sm:flex-row sm:items-center justify-between gap-4 shadow-lg">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 rounded-xl bg-cyan-500/20 border border-cyan-500/30 flex items-center justify-center text-cyan-400 flex-shrink-0">
              <Target className="w-6 h-6" />
            </div>
            <div>
              <div className="text-[10px] uppercase font-bold tracking-wider text-cyan-400">High-Priority Next Action</div>
              <h3 className="text-base font-bold text-white mt-0.5">{summary.recommended_next_action.title}</h3>
              <p className="text-xs text-slate-300 mt-1 max-w-2xl">{summary.recommended_next_action.description}</p>
            </div>
          </div>
          <Link
            to={summary.recommended_next_action.link}
            className="inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl font-bold text-xs bg-cyan-500 hover:bg-cyan-400 text-slate-950 transition shadow-md whitespace-nowrap self-start sm:self-center"
          >
            <span>{summary.recommended_next_action.action_text}</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      )}

      {/* KPI Cards Row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 shadow">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Profile Completeness</span>
            <UserCheck className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-2xl font-black text-white font-mono">{summary.profile_completion_pct}%</div>
          <div className="w-full bg-slate-800 h-1.5 rounded-full mt-3 overflow-hidden">
            <div
              className="bg-cyan-400 h-full rounded-full transition-all duration-500"
              style={{ width: `${summary.profile_completion_pct}%` }}
            ></div>
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 shadow">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Technical Skills</span>
            <Award className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-2xl font-black text-white font-mono">{summary.total_skills_count}</div>
          <p className="text-xs text-slate-400 mt-2">
            <span className="text-teal-400 font-bold">{summary.verified_skills_count}</span> verified by test
          </p>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 shadow">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Roadmap Progress</span>
            <Milestone className="w-4 h-4 text-teal-400" />
          </div>
          <div className="text-2xl font-black text-white font-mono">{summary.roadmap_progress_pct}%</div>
          <div className="w-full bg-slate-800 h-1.5 rounded-full mt-3 overflow-hidden">
            <div
              className="bg-teal-400 h-full rounded-full transition-all duration-500"
              style={{ width: `${summary.roadmap_progress_pct}%` }}
            ></div>
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 shadow">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Assessments Taken</span>
            <CheckCircle2 className="w-4 h-4 text-violet-400" />
          </div>
          <div className="text-2xl font-black text-white font-mono">{summary.completed_assessments_count}</div>
          <p className="text-xs text-slate-400 mt-2">
            Avg Score: <span className="text-violet-300 font-bold">{summary.average_assessment_score}%</span>
          </p>
        </div>
      </div>

      {/* Visual Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Radar Chart: Category Proficiency */}
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-base font-bold text-white">Student Capability Radar</h3>
              <p className="text-xs text-slate-400">Proficiency across computer science disciplines</p>
            </div>
            <span className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-400 font-mono">0 - 100</span>
          </div>

          <div className="h-64 sm:h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid stroke="#334155" />
                <PolarAngleAxis dataKey="category" stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 11 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#475569" />
                <Radar
                  name="Proficiency"
                  dataKey="score"
                  stroke="#06b6d4"
                  fill="#06b6d4"
                  fillOpacity={0.4}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Skill Gap Matrix Bar Chart */}
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-base font-bold text-white">Skill Gap Breakdown for {summary.target_role}</h3>
              <p className="text-xs text-slate-400">Required competency status based on role benchmarks</p>
            </div>
            <Link to="/analysis" className="text-xs font-semibold text-cyan-400 hover:text-cyan-300 flex items-center gap-1">
              <span>Full Matrix</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="h-64 sm:h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={gapChartData} layout="vertical" margin={{ top: 10, right: 30, left: 40, bottom: 5 }}>
                <XAxis type="number" stroke="#475569" tick={{ fill: '#94a3b8', fontSize: 11 }} />
                <YAxis dataKey="name" type="category" stroke="#475569" tick={{ fill: '#94a3b8', fontSize: 11 }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '0.75rem', color: '#fff' }}
                />
                <Bar dataKey="count" radius={[0, 8, 8, 0]}>
                  {gapChartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Bottom Section: Recent Activity & Action Quick Links */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Recent Activity Timeline */}
        <div className="lg:col-span-2 p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow">
          <div className="flex items-center justify-between mb-5">
            <div className="flex items-center gap-2">
              <Activity className="w-4 h-4 text-cyan-400" />
              <h3 className="text-base font-bold text-white">Recent Student Activity Logs</h3>
            </div>
            <span className="text-xs text-slate-400">Real verified actions</span>
          </div>

          {summary.recent_activities && summary.recent_activities.length > 0 ? (
            <div className="space-y-4">
              {summary.recent_activities.map((act) => (
                <div key={act.id} className="flex items-start gap-3 pb-3 border-b border-slate-800/80 last:border-none">
                  <div className="w-2 h-2 rounded-full bg-cyan-400 mt-1.5 flex-shrink-0"></div>
                  <div className="flex-1">
                    <p className="text-xs text-slate-200 font-medium">{act.description}</p>
                    <span className="text-[10px] text-slate-400 font-mono mt-0.5 block">
                      {new Date(act.created_at).toLocaleString()}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="p-8 text-center text-slate-400 text-xs">
              No recent activity recorded yet. Start by taking an assessment or adding skills!
            </div>
          )}
        </div>

        {/* Quick Hub Navigation Cards */}
        <div className="space-y-4">
          <Link
            to="/assessments"
            className="block p-5 rounded-2xl bg-slate-900 border border-slate-800 hover:border-cyan-500/40 transition group"
          >
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-cyan-400">Skill Assessments</span>
              <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-cyan-400 group-hover:translate-x-1 transition" />
            </div>
            <p className="text-sm font-bold text-white mt-2">Take Structured MCQ Tests</p>
            <p className="text-xs text-slate-400 mt-1">Validate your self-reported skill proficiency with objective test records.</p>
          </Link>

          <Link
            to="/roadmap"
            className="block p-5 rounded-2xl bg-slate-900 border border-slate-800 hover:border-teal-500/40 transition group"
          >
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-teal-400">Personalized Roadmap</span>
              <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-teal-400 group-hover:translate-x-1 transition" />
            </div>
            <p className="text-sm font-bold text-white mt-2">Phased Learning Curriculum</p>
            <p className="text-xs text-slate-400 mt-1">Follow curated tasks and mark your progress week by week.</p>
          </Link>

          <Link
            to="/interview"
            className="block p-5 rounded-2xl bg-slate-900 border border-slate-800 hover:border-violet-500/40 transition group"
          >
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-violet-400">Interview Studio</span>
              <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-violet-400 group-hover:translate-x-1 transition" />
            </div>
            <p className="text-sm font-bold text-white mt-2">Practice Technical Questions</p>
            <p className="text-xs text-slate-400 mt-1">Submit your answers for AI-powered rubric scoring and model answers.</p>
          </Link>
        </div>
      </div>
    </div>
  );
}
