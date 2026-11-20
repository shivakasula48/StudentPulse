import React from 'react';
import { Link } from 'react-router-dom';
import {
  BrainCircuit,
  Compass,
  ArrowRight,
  ShieldCheck,
  CheckCircle2,
  GitCompare,
  Milestone,
  FolderKanban,
  MessageSquareCode,
  Sparkles,
  Layers,
  TrendingUp,
  Award,
  BookOpen,
  ChevronRight
} from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-cyan-500 selection:text-white">
      {/* Navigation */}
      <header className="border-b border-slate-800/80 bg-slate-900/60 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-cyan-500/20 text-white font-bold">
              <BrainCircuit className="w-6 h-6 text-white" />
            </div>
            <div>
              <span className="font-extrabold text-xl tracking-tight bg-gradient-to-r from-cyan-400 via-sky-300 to-indigo-400 bg-clip-text text-transparent">
                StudentPulse<span className="text-cyan-400"> AI</span>
              </span>
              <div className="text-[10px] uppercase font-bold tracking-widest text-slate-400">Team Byte Force</div>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <Link
              to="/login"
              className="text-sm font-semibold text-slate-300 hover:text-white px-4 py-2 rounded-lg transition"
            >
              Sign In
            </Link>
            <Link
              to="/register"
              className="text-sm font-semibold bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white px-5 py-2.5 rounded-xl shadow-lg shadow-cyan-500/25 transition transform hover:-translate-y-0.5"
            >
              Get Started Free
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative pt-20 pb-24 overflow-hidden border-b border-slate-800/60">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(14,165,233,0.15),rgba(255,255,255,0))]"></div>
        <div className="max-w-5xl mx-auto px-6 text-center relative z-10">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-cyan-950/70 border border-cyan-800/60 text-cyan-300 text-xs font-semibold mb-8 backdrop-blur-sm">
            <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
            <span>AI-Powered Student Success, Skill & Career Readiness Platform</span>
          </div>

          <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-white leading-tight sm:leading-none">
            Discover Your Skills. <br />
            <span className="bg-gradient-to-r from-cyan-400 via-sky-300 to-indigo-400 bg-clip-text text-transparent">
              Identify Your Gaps.
            </span> <br />
            Build Your Future.
          </h1>

          <p className="mt-6 text-lg sm:text-xl text-slate-300 max-w-3xl mx-auto font-normal leading-relaxed">
            The intelligent EdTech SaaS that bridges the gap between college coursework and industry expectations through a transparent, evidence-based methodology.
          </p>

          <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              to="/register"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 text-base font-bold bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white px-8 py-4 rounded-xl shadow-xl shadow-cyan-500/25 transition transform hover:-translate-y-0.5"
            >
              <span>Get Started Now</span>
              <ArrowRight className="w-5 h-5" />
            </Link>
            <Link
              to="/login"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 text-base font-semibold bg-slate-900 hover:bg-slate-800 border border-slate-700/80 text-slate-200 px-7 py-4 rounded-xl transition"
            >
              <span>Explore Dashboard</span>
            </Link>
          </div>

          {/* Philosophy Banner */}
          <div className="mt-16 p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-2xl backdrop-blur-sm grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
            <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80">
              <div className="text-xs font-bold uppercase tracking-wider text-cyan-400 flex items-center gap-2">
                <span className="w-6 h-6 rounded-lg bg-cyan-950 flex items-center justify-center text-cyan-400 font-mono">1</span>
                <span>EVIDENCE</span>
              </div>
              <h3 className="mt-2 text-base font-bold text-white">Unified Student Inventory</h3>
              <p className="mt-1 text-xs text-slate-400 leading-relaxed">
                Collect self-reported competencies, academic details, verified assessment tests, and previous projects.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80">
              <div className="text-xs font-bold uppercase tracking-wider text-indigo-400 flex items-center gap-2">
                <span className="w-6 h-6 rounded-lg bg-indigo-950 flex items-center justify-center text-indigo-400 font-mono">2</span>
                <span>INSIGHT</span>
              </div>
              <h3 className="mt-2 text-base font-bold text-white">Deterministic Gap Analysis</h3>
              <p className="mt-1 text-xs text-slate-400 leading-relaxed">
                Compare actual student abilities against role-specific benchmarks with transparent AI explanations.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80">
              <div className="text-xs font-bold uppercase tracking-wider text-teal-400 flex items-center gap-2">
                <span className="w-6 h-6 rounded-lg bg-teal-950 flex items-center justify-center text-teal-400 font-mono">3</span>
                <span>ACTION</span>
              </div>
              <h3 className="mt-2 text-base font-bold text-white">Personalized Readiness Plans</h3>
              <p className="mt-1 text-xs text-slate-400 leading-relaxed">
                Generate phased learning roadmaps, portfolio project recommendations, and AI interview prep sessions.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Core Features */}
      <section className="py-20 bg-slate-900/30 border-b border-slate-800/60">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-xs font-bold uppercase tracking-widest text-cyan-400">Comprehensive Modules</h2>
            <p className="mt-2 text-3xl sm:text-4xl font-extrabold text-white">
              Everything Needed for College to Career Transition
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="p-7 rounded-2xl bg-slate-900 border border-slate-800 hover:border-cyan-500/40 transition">
              <div className="w-12 h-12 rounded-xl bg-cyan-950/80 border border-cyan-800/60 flex items-center justify-center text-cyan-400 mb-5">
                <GitCompare className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-bold text-white">Role-Based Gap Matrix</h3>
              <p className="mt-2 text-sm text-slate-400 leading-relaxed">
                Choose from target roles like Java Developer, Python Dev, Full Stack, Data Analyst, or AI/ML Engineer. Understand strong vs missing skills.
              </p>
            </div>

            <div className="p-7 rounded-2xl bg-slate-900 border border-slate-800 hover:border-indigo-500/40 transition">
              <div className="w-12 h-12 rounded-xl bg-indigo-950/80 border border-indigo-800/60 flex items-center justify-center text-indigo-400 mb-5">
                <CheckCircle2 className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-bold text-white">Verified Skill Assessments</h3>
              <p className="mt-2 text-sm text-slate-400 leading-relaxed">
                Separate self-reported levels from verified performance. Take structured MCQs across 8 core computer science categories.
              </p>
            </div>

            <div className="p-7 rounded-2xl bg-slate-900 border border-slate-800 hover:border-teal-500/40 transition">
              <div className="w-12 h-12 rounded-xl bg-teal-950/80 border border-teal-800/60 flex items-center justify-center text-teal-400 mb-5">
                <Milestone className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-bold text-white">Dynamic Learning Roadmap</h3>
              <p className="mt-2 text-sm text-slate-400 leading-relaxed">
                Receive customized, phased curricula with durations, learning objectives, verified resources, and real-time status toggles.
              </p>
            </div>

            <div className="p-7 rounded-2xl bg-slate-900 border border-slate-800 hover:border-amber-500/40 transition">
              <div className="w-12 h-12 rounded-xl bg-amber-950/80 border border-amber-800/60 flex items-center justify-center text-amber-400 mb-5">
                <FolderKanban className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-bold text-white">Curated Project Hub</h3>
              <p className="mt-2 text-sm text-slate-400 leading-relaxed">
                Discover hands-on project blueprints tailored to address specific skill gaps, with 1-click adoption into your portfolio tracker.
              </p>
            </div>

            <div className="p-7 rounded-2xl bg-slate-900 border border-slate-800 hover:border-violet-500/40 transition">
              <div className="w-12 h-12 rounded-xl bg-violet-950/80 border border-violet-800/60 flex items-center justify-center text-violet-400 mb-5">
                <MessageSquareCode className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-bold text-white">AI Interview Prep Studio</h3>
              <p className="mt-2 text-sm text-slate-400 leading-relaxed">
                Simulate role-specific technical and behavioral interviews with transparent rubric feedback, strengths, and exemplar model answers.
              </p>
            </div>

            <div className="p-7 rounded-2xl bg-slate-900 border border-slate-800 hover:border-emerald-500/40 transition">
              <div className="w-12 h-12 rounded-xl bg-emerald-950/80 border border-emerald-800/60 flex items-center justify-center text-emerald-400 mb-5">
                <TrendingUp className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-bold text-white">Genuine Career Readiness Index</h3>
              <p className="mt-2 text-sm text-slate-400 leading-relaxed">
                No fake percentages. Readiness scores are calculated from verified assessment tests, role alignment, roadmap progress, and portfolio evidence.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-slate-950 border-t border-slate-800 text-slate-400 text-sm">
        <div className="max-w-7xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-cyan-500 to-indigo-600 flex items-center justify-center text-white font-bold text-sm">
              <BrainCircuit className="w-5 h-5 text-white" />
            </div>
            <span className="font-bold text-slate-200">StudentPulse AI</span>
            <span className="text-xs bg-slate-800 px-2.5 py-0.5 rounded-full text-slate-400 font-mono">Team Byte Force</span>
          </div>
          <p className="text-xs text-slate-400 text-center sm:text-right">
            Designed and engineered for college student career readiness and success. Powered by Google Gemini.
          </p>
        </div>
      </footer>
    </div>
  );
}
