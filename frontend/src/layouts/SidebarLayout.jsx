import React, { useState } from 'react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  LayoutDashboard,
  UserCheck,
  Award,
  CheckCircle2,
  GitCompare,
  Milestone,
  FolderKanban,
  MessageSquareCode,
  BookOpen,
  LogOut,
  Menu,
  X,
  Sparkles,
  Target,
  ChevronRight,
  ShieldCheck,
  BrainCircuit
} from 'lucide-react';

const navigationItems = [
  { name: 'Readiness Dashboard', path: '/dashboard', icon: LayoutDashboard },
  { name: 'Student Profile', path: '/profile', icon: UserCheck },
  { name: 'Skills Inventory', path: '/skills', icon: Award },
  { name: 'Skill Assessments', path: '/assessments', icon: CheckCircle2 },
  { name: 'AI Skill Gap Analysis', path: '/analysis', icon: GitCompare },
  { name: 'Learning Roadmap', path: '/roadmap', icon: Milestone },
  { name: 'Project Hub', path: '/projects', icon: FolderKanban },
  { name: 'AI Interview Studio', path: '/interview', icon: MessageSquareCode },
  { name: 'Resource Library', path: '/resources', icon: BookOpen },
];

export default function SidebarLayout() {
  const { user, logout, systemInfo } = useAuth();
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isLiveAI = systemInfo?.ai_engine?.connected;

  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 overflow-hidden font-sans">
      {/* Mobile menu backdrop */}
      {mobileMenuOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/70 backdrop-blur-sm lg:hidden"
          onClick={() => setMobileMenuOpen(false)}
        />
      )}

      {/* Sidebar navigation */}
      <aside
        className={`fixed inset-y-0 left-0 z-50 w-72 bg-slate-900 border-r border-slate-800/80 flex flex-col transition-transform duration-300 lg:static lg:translate-x-0 ${
          mobileMenuOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Brand header */}
        <div className="flex items-center justify-between h-20 px-6 border-b border-slate-800/80 bg-slate-900/60">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-cyan-500/20 text-white font-bold text-xl">
              <BrainCircuit className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-cyan-400 via-sky-300 to-indigo-400 bg-clip-text text-transparent">
                StudentPulse<span className="text-cyan-400"> AI</span>
              </div>
              <div className="text-[10px] uppercase font-bold tracking-widest text-slate-400 flex items-center gap-1">
                <span>By Byte Force</span>
                <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-pulse"></span>
              </div>
            </div>
          </div>
          <button
            onClick={() => setMobileMenuOpen(false)}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 lg:hidden"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Method badge */}
        <div className="px-5 py-3 border-b border-slate-800/60 bg-slate-950/40">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider flex items-center justify-between">
            <span>Framework</span>
            <span className="text-cyan-400 font-mono text-[10px]">v1.0-MSE2</span>
          </div>
          <div className="mt-1 flex items-center gap-1.5 text-xs text-slate-300 font-medium">
            <span className="text-cyan-400 font-bold">Evidence</span>
            <ChevronRight className="w-3 h-3 text-slate-600" />
            <span className="text-indigo-400 font-bold">Insight</span>
            <ChevronRight className="w-3 h-3 text-slate-600" />
            <span className="text-teal-400 font-bold">Action</span>
          </div>
        </div>

        {/* Navigation Links */}
        <nav className="flex-1 px-4 py-4 space-y-1 overflow-y-auto scrollbar-thin scrollbar-thumb-slate-800">
          {navigationItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={() => setMobileMenuOpen(false)}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all ${
                    isActive
                      ? 'bg-gradient-to-r from-cyan-500/20 to-indigo-500/10 text-cyan-400 border border-cyan-500/30 shadow-sm'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                  }`
                }
              >
                <Icon className="w-4 h-4 flex-shrink-0" />
                <span>{item.name}</span>
              </NavLink>
            );
          })}
        </nav>

        {/* Engine status & user footer */}
        <div className="p-4 border-t border-slate-800/80 bg-slate-950/40">
          {/* AI Status */}
          <div className="mb-3 px-3 py-2 rounded-lg bg-slate-900 border border-slate-800 flex items-center justify-between text-xs">
            <div className="flex items-center gap-2">
              <span className={`w-2 h-2 rounded-full ${isLiveAI ? 'bg-teal-400 shadow-sm shadow-teal-400/50' : 'bg-amber-400'}`}></span>
              <span className="text-slate-300 font-medium text-[11px]">
                {isLiveAI ? 'Gemini 4 AI Live' : 'Deterministic Engine'}
              </span>
            </div>
            <span className="text-[10px] text-slate-400 font-mono">
              {isLiveAI ? 'Connected' : 'Fallback Ready'}
            </span>
          </div>

          {/* User profile info & logout */}
          <div className="flex items-center justify-between pt-1">
            <div className="flex items-center gap-3 overflow-hidden">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold text-sm shadow">
                {user?.name ? user.name[0].toUpperCase() : 'S'}
              </div>
              <div className="truncate">
                <p className="text-sm font-semibold text-slate-200 truncate">{user?.name || 'Student'}</p>
                <p className="text-xs text-slate-400 truncate">{user?.email || ''}</p>
              </div>
            </div>
            <button
              onClick={handleLogout}
              title="Sign Out"
              className="p-2 text-slate-400 hover:text-red-400 hover:bg-slate-800/80 rounded-lg transition"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      </aside>

      {/* Main content area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Top bar */}
        <header className="h-16 bg-slate-900/50 backdrop-blur-md border-b border-slate-800/80 px-6 flex items-center justify-between z-10">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setMobileMenuOpen(true)}
              className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 lg:hidden"
            >
              <Menu className="w-5 h-5" />
            </button>
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-400 font-medium">Target Career Goal:</span>
              <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-cyan-950/60 border border-cyan-800/60 text-cyan-300 text-xs font-semibold">
                <Target className="w-3.5 h-3.5 text-cyan-400" />
                <span>{user?.target_role || 'Java Developer'}</span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="hidden sm:flex items-center gap-2 px-3 py-1 rounded-lg bg-slate-800/60 border border-slate-700/60 text-slate-300 text-xs">
              <ShieldCheck className="w-3.5 h-3.5 text-teal-400" />
              <span>Evidence-Backed Verification</span>
            </div>
          </div>
        </header>

        {/* Dynamic page outlet */}
        <main className="flex-1 overflow-y-auto bg-slate-950 p-6 md:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
