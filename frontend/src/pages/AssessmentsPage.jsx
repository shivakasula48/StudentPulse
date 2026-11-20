import React, { useState, useEffect } from 'react';
import api from '../services/api';
import {
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  ArrowRight,
  ArrowLeft,
  RotateCcw,
  Award,
  Clock,
  Sparkles,
  ShieldCheck,
  Code,
  Binary,
  Database,
  Globe,
  Cpu,
  Brain,
  MessageSquare,
  Lightbulb,
  Check,
  X
} from 'lucide-react';

const iconMap = {
  Code: Code,
  Binary: Binary,
  Database: Database,
  Globe: Globe,
  Cpu: Cpu,
  Brain: Brain,
  MessageSquare: MessageSquare,
  Lightbulb: Lightbulb
};

export default function AssessmentsPage() {
  const [categories, setCategories] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Active Assessment State
  const [activeCategory, setActiveCategory] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({}); // { question_id: 'A' }
  const [submitting, setSubmitting] = useState(false);
  const [assessmentResult, setAssessmentResult] = useState(null);

  const fetchAssessmentsData = async () => {
    try {
      setLoading(true);
      const [catRes, histRes] = await Promise.all([
        api.get('/assessments/categories'),
        api.get('/assessments/results')
      ]);
      setCategories(catRes.data);
      setHistory(histRes.data);
    } catch (err) {
      console.error(err);
      setError('Failed to load assessment modules.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAssessmentsData();
  }, []);

  const startAssessment = async (categoryTitle) => {
    try {
      setLoading(true);
      setError('');
      const res = await api.get(`/assessments/questions?category=${encodeURIComponent(categoryTitle)}`);
      setQuestions(res.data);
      setActiveCategory(categoryTitle);
      setCurrentQuestionIndex(0);
      setSelectedAnswers({});
      setAssessmentResult(null);
    } catch (err) {
      setError(`Failed to load questions for ${categoryTitle}.`);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectOption = (questionId, optionLetter) => {
    setSelectedAnswers({
      ...selectedAnswers,
      [questionId]: optionLetter
    });
  };

  const handleSubmitAssessment = async () => {
    const answeredCount = Object.keys(selectedAnswers).length;
    if (answeredCount < questions.length) {
      if (!window.confirm(`You answered ${answeredCount} of ${questions.length} questions. Submit anyway?`)) {
        return;
      }
    }

    try {
      setSubmitting(true);
      const submissionPayload = {
        category: activeCategory,
        answers: questions.map((q) => ({
          question_id: q.id,
          selected_answer: selectedAnswers[q.id] || 'A'
        }))
      };

      const res = await api.post('/assessments/submit', submissionPayload);
      setAssessmentResult(res.data);
      fetchAssessmentsData(); // Refresh history
    } catch (err) {
      setError('Failed to evaluate assessment submission.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleExitQuiz = () => {
    setActiveCategory(null);
    setQuestions([]);
    setAssessmentResult(null);
  };

  if (loading && !activeCategory) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="w-10 h-10 border-4 border-cyan-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  // --- VIEW 1: Active Assessment Studio ---
  if (activeCategory && questions.length > 0 && !assessmentResult) {
    const currentQ = questions[currentQuestionIndex];
    const progressPct = ((currentQuestionIndex + 1) / questions.length) * 100;
    const currentSelected = selectedAnswers[currentQ.id];

    return (
      <div className="max-w-3xl mx-auto space-y-6 pb-12">
        {/* Studio Top Header */}
        <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-between">
          <div>
            <span className="text-[10px] uppercase font-bold tracking-wider text-cyan-400">
              Verified Skill Assessment
            </span>
            <h2 className="text-lg font-bold text-white">{activeCategory}</h2>
          </div>
          <button
            onClick={handleExitQuiz}
            className="text-xs text-slate-400 hover:text-white px-3 py-1.5 rounded-lg bg-slate-800"
          >
            Cancel & Exit
          </button>
        </div>

        {/* Progress Bar */}
        <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
          <div
            className="bg-cyan-500 h-full transition-all duration-300"
            style={{ width: `${progressPct}%` }}
          ></div>
        </div>

        {/* Question Card */}
        <div className="p-6 sm:p-8 rounded-3xl bg-slate-900 border border-slate-800 shadow-xl space-y-6">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>
              Question <span className="font-bold text-white">{currentQuestionIndex + 1}</span> of {questions.length}
            </span>
            <span className="px-2.5 py-0.5 rounded-full bg-slate-800 font-mono text-[11px] text-cyan-300">
              {currentQ.difficulty} • Skill: {currentQ.skill_name}
            </span>
          </div>

          <h3 className="text-lg sm:text-xl font-bold text-white leading-relaxed">
            {currentQ.question_text}
          </h3>

          {/* Options */}
          <div className="space-y-3 pt-2">
            {[
              { key: 'A', text: currentQ.option_a },
              { key: 'B', text: currentQ.option_b },
              { key: 'C', text: currentQ.option_c },
              { key: 'D', text: currentQ.option_d }
            ].map((opt) => (
              <button
                key={opt.key}
                type="button"
                onClick={() => handleSelectOption(currentQ.id, opt.key)}
                className={`w-full p-4 rounded-xl text-left text-sm font-medium transition flex items-center gap-3 border ${
                  currentSelected === opt.key
                    ? 'bg-cyan-500/10 border-cyan-500 text-cyan-300 shadow-sm'
                    : 'bg-slate-950/60 border-slate-800 text-slate-300 hover:bg-slate-800/80 hover:border-slate-700'
                }`}
              >
                <span
                  className={`w-7 h-7 rounded-lg flex items-center justify-center font-bold text-xs flex-shrink-0 ${
                    currentSelected === opt.key
                      ? 'bg-cyan-500 text-slate-950'
                      : 'bg-slate-800 text-slate-400'
                  }`}
                >
                  {opt.key}
                </span>
                <span className="flex-1">{opt.text}</span>
              </button>
            ))}
          </div>

          {/* Controls */}
          <div className="pt-4 border-t border-slate-800 flex items-center justify-between">
            <button
              onClick={() => setCurrentQuestionIndex((prev) => Math.max(0, prev - 1))}
              disabled={currentQuestionIndex === 0}
              className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-slate-800 text-slate-300 text-xs font-semibold disabled:opacity-40"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Previous</span>
            </button>

            {currentQuestionIndex < questions.length - 1 ? (
              <button
                onClick={() => setCurrentQuestionIndex((prev) => Math.min(questions.length - 1, prev + 1))}
                className="flex items-center gap-1.5 px-5 py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 text-xs font-bold shadow"
              >
                <span>Next Question</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            ) : (
              <button
                onClick={handleSubmitAssessment}
                disabled={submitting}
                className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-teal-400 to-emerald-500 hover:from-teal-300 hover:to-emerald-400 text-slate-950 font-extrabold text-xs shadow-lg transition"
              >
                {submitting ? 'Scoring Answers...' : 'Submit & Calculate Score'}
                <CheckCircle2 className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>
      </div>
    );
  }

  // --- VIEW 2: Assessment Results Modal / View ---
  if (assessmentResult) {
    return (
      <div className="max-w-3xl mx-auto space-y-6 pb-12">
        <div className="p-6 sm:p-8 rounded-3xl bg-slate-900 border border-slate-800 text-center shadow-2xl space-y-4">
          <div className="w-16 h-16 rounded-2xl bg-teal-500/20 border border-teal-500/30 text-teal-400 mx-auto flex items-center justify-center">
            <Award className="w-8 h-8" />
          </div>

          <h2 className="text-2xl font-black text-white">Assessment Completed</h2>
          <p className="text-sm text-slate-400 max-w-md mx-auto">
            Category: <span className="text-white font-bold">{assessmentResult.category}</span>
          </p>

          <div className="py-4">
            <div className="text-5xl font-black text-white font-mono">
              {assessmentResult.score.toFixed(0)}%
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Verified test score updated on your student capability inventory.
            </p>
          </div>

          <button
            onClick={handleExitQuiz}
            className="px-6 py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs shadow transition"
          >
            Return to Assessment Hub
          </button>
        </div>

        {/* Detailed Question Answers with Explanations */}
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 space-y-4">
          <h3 className="text-base font-bold text-white pb-3 border-b border-slate-800">
            Performance Breakdown & Explanations
          </h3>

          {assessmentResult.answers && assessmentResult.answers.map((ans, idx) => (
            <div
              key={idx}
              className={`p-4 rounded-xl border ${
                ans.is_correct ? 'bg-teal-950/20 border-teal-800/40' : 'bg-red-950/20 border-red-800/40'
              }`}
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex items-center gap-2">
                  <span
                    className={`w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold ${
                      ans.is_correct ? 'bg-teal-500 text-slate-950' : 'bg-red-500 text-white'
                    }`}
                  >
                    {ans.is_correct ? <Check className="w-3 h-3" /> : <X className="w-3 h-3" />}
                  </span>
                  <span className="text-xs font-bold text-white">Question {idx + 1} ({ans.skill_name})</span>
                </div>
                <span className="text-[11px] font-mono text-slate-400">
                  Your Answer: <strong className={ans.is_correct ? 'text-teal-400' : 'text-red-400'}>{ans.selected_answer}</strong> | Correct: <strong className="text-teal-400">{ans.correct_option}</strong>
                </span>
              </div>

              <p className="text-xs text-slate-200 mt-2 font-medium">{ans.question_text}</p>
              {ans.explanation && (
                <div className="mt-2 text-[11px] text-slate-400 bg-slate-950/60 p-2.5 rounded-lg border border-slate-800">
                  <strong className="text-slate-300">Explanation:</strong> {ans.explanation}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    );
  }

  // --- VIEW 3: Category Selection Hub ---
  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-12">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Objective Skill Assessments
          </h1>
          <p className="mt-1 text-sm text-slate-400">
            Validate your theoretical and practical competencies through structured multi-choice evaluations.
          </p>
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-red-950/60 border border-red-800/80 text-red-300 text-sm flex items-center gap-3">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Category Selection Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {categories.map((cat) => {
          const Icon = iconMap[cat.icon] || Code;
          return (
            <div
              key={cat.id}
              className="p-5 rounded-2xl bg-slate-900 border border-slate-800 hover:border-cyan-500/50 transition flex flex-col justify-between group"
            >
              <div>
                <div className="w-10 h-10 rounded-xl bg-cyan-950 border border-cyan-800/60 flex items-center justify-center text-cyan-400 mb-4 group-hover:scale-105 transition">
                  <Icon className="w-5 h-5" />
                </div>
                <h3 className="font-bold text-white text-base">{cat.title}</h3>
                <p className="text-xs text-slate-400 mt-1.5 leading-relaxed">{cat.description}</p>
              </div>

              <div className="mt-6 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span className="text-[11px] text-slate-500 font-mono">{cat.total_questions} Questions</span>
                <button
                  onClick={() => startAssessment(cat.id)}
                  className="px-3.5 py-1.5 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs shadow transition flex items-center gap-1"
                >
                  <span>Start Test</span>
                  <ArrowRight className="w-3 h-3" />
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* Completed Test History Table */}
      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow">
        <h2 className="text-lg font-bold text-white mb-4">Past Verified Assessment History</h2>

        {history && history.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400 font-semibold uppercase">
                  <th className="pb-3">Category</th>
                  <th className="pb-3">Questions</th>
                  <th className="pb-3">Verified Score</th>
                  <th className="pb-3">Status</th>
                  <th className="pb-3">Date Completed</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {history.map((h) => (
                  <tr key={h.id} className="hover:bg-slate-800/30 transition">
                    <td className="py-3 font-semibold text-white">{h.category}</td>
                    <td className="py-3 text-slate-300 font-mono">{h.total_questions}</td>
                    <td className="py-3 font-bold font-mono text-cyan-400">{h.score.toFixed(0)}%</td>
                    <td className="py-3">
                      <span
                        className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                          h.score >= 70
                            ? 'bg-teal-950 text-teal-400 border border-teal-800/60'
                            : 'bg-amber-950 text-amber-400 border border-amber-800/60'
                        }`}
                      >
                        {h.score >= 70 ? 'Passed' : 'Needs Review'}
                      </span>
                    </td>
                    <td className="py-3 text-slate-400">{new Date(h.completed_at).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-xs text-slate-500 italic py-4">No assessment records found. Take your first test above!</p>
        )}
      </div>
    </div>
  );
}
