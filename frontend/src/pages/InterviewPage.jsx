import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import {
  MessageSquareCode,
  Sparkles,
  HelpCircle,
  Send,
  Award,
  CheckCircle2,
  AlertTriangle,
  Lightbulb,
  Clock,
  RotateCcw,
  AlertCircle,
  ChevronDown,
  ChevronUp
} from 'lucide-react';

export default function InterviewPage() {
  const { user } = useAuth();
  const [categories, setCategories] = useState([]);
  const [selectedRole, setSelectedRole] = useState(user?.target_role || 'Java Developer');
  const [selectedCategory, setSelectedCategory] = useState('Technical Interview');
  const [difficulty, setDifficulty] = useState('Intermediate');

  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [studentAnswer, setStudentAnswer] = useState('');
  const [showHint, setShowHint] = useState(false);

  const [evaluating, setEvaluating] = useState(false);
  const [evaluationResult, setEvaluationResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchInterviewData = async () => {
    try {
      setLoading(true);
      const [catRes, histRes] = await Promise.all([
        api.get('/interview/categories'),
        api.get('/interview/history')
      ]);
      setCategories(catRes.data);
      setHistory(histRes.data);
      if (catRes.data.length > 0) {
        setSelectedCategory(catRes.data[0].id);
      }
    } catch (err) {
      console.error(err);
      setError('Failed to load interview studio.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInterviewData();
  }, []);

  // Generate question when role or category changes
  const handleGenerateQuestion = async () => {
    try {
      setLoading(true);
      setError('');
      setEvaluationResult(null);
      setStudentAnswer('');
      setShowHint(false);

      const res = await api.post('/interview/generate', {
        target_role: selectedRole,
        category: selectedCategory,
        difficulty: difficulty
      });

      setQuestions(res.data);
      if (res.data.length > 0) {
        setCurrentQuestion(res.data[0]);
      }
    } catch (err) {
      setError('Failed to generate interview question.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedCategory) {
      handleGenerateQuestion();
    }
  }, [selectedCategory, selectedRole]);

  const handleSubmitAnswer = async (e) => {
    e.preventDefault();
    if (!studentAnswer.trim() || studentAnswer.trim().length < 5) {
      setError('Please provide a substantive answer for evaluation.');
      return;
    }

    try {
      setEvaluating(true);
      setError('');
      const res = await api.post('/interview/evaluate', {
        target_role: selectedRole,
        category: selectedCategory,
        question: currentQuestion.question,
        student_answer: studentAnswer
      });
      setEvaluationResult(res.data);

      // Refresh history
      const histRes = await api.get('/interview/history');
      setHistory(histRes.data);
    } catch (err) {
      setError('Evaluation failed. Please try again.');
    } finally {
      setEvaluating(false);
    }
  };

  return (
    <div className="space-y-8 max-w-5xl mx-auto pb-12">
      {/* Top Banner */}
      <div className="p-6 sm:p-8 rounded-3xl bg-slate-900 border border-slate-800 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-violet-950/80 border border-violet-800/60 text-violet-400 text-xs font-semibold mb-2">
            <Sparkles className="w-3.5 h-3.5" />
            <span>AI Mock Technical Interview & Rubric Evaluation</span>
          </div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight">
            Interview Preparation Studio
          </h1>
          <p className="text-xs text-slate-400 mt-1 max-w-xl">
            Rehearse technical concepts, OOP architecture, and scenario-based questions with instant AI coaching feedback.
          </p>
        </div>

        {/* Role & Category Selectors */}
        <div className="flex flex-wrap items-center gap-3">
          <select
            value={selectedRole}
            onChange={(e) => setSelectedRole(e.target.value)}
            className="px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-cyan-300 font-bold text-xs outline-none"
          >
            <option value="Java Developer">Java Developer</option>
            <option value="Python Developer">Python Developer</option>
            <option value="Full Stack Developer">Full Stack Developer</option>
            <option value="Data Analyst">Data Analyst</option>
            <option value="Software Engineer">Software Engineer</option>
          </select>

          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-violet-300 font-bold text-xs outline-none"
          >
            {categories.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-red-950/60 border border-red-800/80 text-red-300 text-sm flex items-center gap-3">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Active Question Simulator Card */}
      {currentQuestion && (
        <div className="p-6 sm:p-8 rounded-3xl bg-slate-900 border border-slate-800 shadow-xl space-y-6">
          <div className="flex items-center justify-between pb-4 border-b border-slate-800">
            <span className="text-[11px] px-3 py-1 rounded-full bg-slate-950 border border-slate-800 text-violet-300 font-mono font-bold">
              {currentQuestion.category} • {currentQuestion.difficulty}
            </span>
            <button
              onClick={handleGenerateQuestion}
              className="text-xs text-slate-400 hover:text-white flex items-center gap-1 font-semibold"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Next Question</span>
            </button>
          </div>

          <h3 className="text-xl font-bold text-white leading-relaxed">
            {currentQuestion.question}
          </h3>

          {/* Hint Drawer */}
          {currentQuestion.hint && (
            <div>
              <button
                type="button"
                onClick={() => setShowHint(!showHint)}
                className="text-xs text-cyan-400 hover:text-cyan-300 font-semibold flex items-center gap-1.5"
              >
                <Lightbulb className="w-4 h-4" />
                <span>{showHint ? 'Hide Guidance Hint' : 'Show Interviewer Hint'}</span>
              </button>
              {showHint && (
                <div className="mt-2 p-3 rounded-xl bg-cyan-950/40 border border-cyan-800/50 text-cyan-300 text-xs leading-relaxed">
                  {currentQuestion.hint}
                </div>
              )}
            </div>
          )}

          {/* Student Answer Form */}
          <form onSubmit={handleSubmitAnswer} className="space-y-4 pt-2">
            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                Your Spoken / Written Response
              </label>
              <textarea
                rows={5}
                required
                value={studentAnswer}
                onChange={(e) => setStudentAnswer(e.target.value)}
                placeholder="Explain the concept clearly, define the trade-offs, and cite production edge cases..."
                className="w-full p-4 rounded-2xl bg-slate-950 border border-slate-800 text-white text-sm outline-none focus:border-violet-500 font-sans leading-relaxed transition"
              />
            </div>

            <button
              type="submit"
              disabled={evaluating}
              className="flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-violet-500 to-indigo-600 hover:from-violet-400 hover:to-indigo-500 text-white font-bold text-xs shadow-lg shadow-violet-500/25 transition disabled:opacity-50"
            >
              <Send className="w-4 h-4" />
              <span>{evaluating ? 'Analyzing Technical Depth...' : 'Submit Response for Evaluation'}</span>
            </button>
          </form>
        </div>
      )}

      {/* Instant Evaluation Report Card */}
      {evaluationResult && (
        <div className="p-6 sm:p-8 rounded-3xl bg-slate-900 border border-violet-800/60 shadow-2xl space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-800">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-violet-950 border border-violet-800/80 text-violet-300 text-xs font-semibold mb-2">
                <Award className="w-3.5 h-3.5" />
                <span>Objective Rubric Feedback</span>
              </div>
              <h3 className="text-xl font-bold text-white">Evaluation Results</h3>
            </div>

            {/* Score */}
            <div className="flex items-center gap-3">
              <span className="text-xs text-slate-400 uppercase font-semibold">Rubric Rating:</span>
              <span className="text-3xl font-black text-violet-400 font-mono">
                {evaluationResult.rating.toFixed(0)}/100
              </span>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 rounded-2xl bg-slate-950 border border-teal-900/60 space-y-1.5">
              <div className="flex items-center gap-2 text-teal-400 text-xs font-bold uppercase tracking-wider">
                <CheckCircle2 className="w-4 h-4" />
                <span>Articulated Strengths</span>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed">{evaluationResult.strengths}</p>
            </div>

            <div className="p-4 rounded-2xl bg-slate-950 border border-amber-900/60 space-y-1.5">
              <div className="flex items-center gap-2 text-amber-400 text-xs font-bold uppercase tracking-wider">
                <AlertTriangle className="w-4 h-4" />
                <span>Missing Technical Nuances</span>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed">{evaluationResult.missing_concepts}</p>
            </div>
          </div>

          {/* Feedback */}
          <div className="p-4 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-1.5">
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Interviewer Coaching Feedback</h4>
            <p className="text-xs text-slate-300 leading-relaxed">{evaluationResult.feedback}</p>
          </div>

          {/* Model Answer */}
          <div className="p-5 rounded-2xl bg-slate-950 border border-indigo-900/50 space-y-2">
            <h4 className="text-xs font-bold text-indigo-400 uppercase tracking-wider flex items-center gap-2">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Exemplar Industry Model Answer</span>
            </h4>
            <p className="text-xs text-slate-200 leading-relaxed font-sans">{evaluationResult.model_answer}</p>
          </div>
        </div>
      )}

      {/* Historical Practice Sessions */}
      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow space-y-4">
        <h3 className="text-base font-bold text-white">Past Practice Interview Responses</h3>

        {history && history.length > 0 ? (
          <div className="space-y-3">
            {history.map((h, i) => (
              <div key={i} className="p-4 rounded-xl bg-slate-950 border border-slate-800/80 space-y-2">
                <div className="flex items-start justify-between gap-3">
                  <span className="text-xs font-bold text-white">{h.question}</span>
                  <span className="text-xs font-mono font-bold text-violet-400 bg-violet-950 px-2 py-0.5 rounded">
                    {h.score?.toFixed(0)}/100
                  </span>
                </div>
                <p className="text-xs text-slate-400 italic">"{h.student_answer}"</p>
                <div className="flex items-center justify-between text-[10px] text-slate-500 pt-1">
                  <span>Category: {h.category}</span>
                  <span>{new Date(h.created_at).toLocaleDateString()}</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-slate-500 italic py-4">No past practice interviews recorded yet.</p>
        )}
      </div>
    </div>
  );
}
