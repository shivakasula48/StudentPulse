import React, { useState, useEffect } from 'react';
import api from '../services/api';
import {
  Award,
  Plus,
  Trash2,
  CheckCircle2,
  AlertCircle,
  Filter,
  Search,
  ShieldCheck,
  Edit2,
  X
} from 'lucide-react';

export default function SkillsPage() {
  const [skills, setSkills] = useState([]);
  const [catalog, setCatalog] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Filter & Search
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');

  // Add / Edit Modal
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedSkillName, setSelectedSkillName] = useState('');
  const [customSkillName, setCustomSkillName] = useState('');
  const [skillLevel, setSkillLevel] = useState('Intermediate');

  const fetchSkillsData = async () => {
    try {
      setLoading(true);
      const [myRes, catalogRes] = await Promise.all([
        api.get('/skills/my-skills'),
        api.get('/skills')
      ]);
      setSkills(myRes.data);
      setCatalog(catalogRes.data);
    } catch (err) {
      console.error(err);
      setError('Failed to load skills inventory.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSkillsData();
  }, []);

  const handleAddSkill = async (e) => {
    e.preventDefault();
    const nameToAdd = selectedSkillName === 'custom' ? customSkillName.trim() : selectedSkillName;
    if (!nameToAdd) {
      setError('Please choose or enter a skill name.');
      return;
    }

    try {
      await api.post('/skills/my-skills', {
        skill_name: nameToAdd,
        self_reported_level: skillLevel
      });
      setShowAddModal(false);
      setSelectedSkillName('');
      setCustomSkillName('');
      setSkillLevel('Intermediate');
      setSuccess(`Added '${nameToAdd}' to your skills inventory.`);
      fetchSkillsData();
      setTimeout(() => setSuccess(''), 4000);
    } catch (err) {
      setError('Failed to add skill.');
    }
  };

  const handleUpdateLevel = async (studentSkillId, newLevel) => {
    try {
      await api.put(`/skills/my-skills/${studentSkillId}`, {
        self_reported_level: newLevel
      });
      fetchSkillsData();
    } catch (err) {
      setError('Failed to update skill level.');
    }
  };

  const handleDeleteSkill = async (studentSkillId) => {
    if (!window.confirm('Remove this skill from your profile?')) return;
    try {
      await api.delete(`/skills/my-skills/${studentSkillId}`);
      fetchSkillsData();
    } catch (err) {
      setError('Failed to remove skill.');
    }
  };

  // Categories
  const categories = ['All', 'Programming', 'Web Development', 'Database', 'Framework', 'Tools', 'AI/ML', 'Professional Skills'];

  // Filtered skills
  const filteredSkills = skills.filter((s) => {
    const matchesCat = selectedCategory === 'All' || s.skill.category.toLowerCase() === selectedCategory.toLowerCase();
    const matchesSearch = s.skill.name.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCat && matchesSearch;
  });

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Skills & Competency Inventory
          </h1>
          <p className="mt-1 text-sm text-slate-400">
            Catalog your technical and professional abilities. Verified scores are populated by objective test assessments.
          </p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs shadow-lg shadow-cyan-500/25 transition self-start sm:self-auto"
        >
          <Plus className="w-4 h-4" />
          <span>Add Skill</span>
        </button>
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

      {/* Legend & Verification Philosophy Notice */}
      <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-4 text-xs">
        <div className="flex items-center gap-2 text-slate-300">
          <ShieldCheck className="w-4 h-4 text-teal-400" />
          <span className="font-semibold">Verification Guarantee:</span>
          <span className="text-slate-400">
            Self-reported proficiency is separated from verified assessment scores to maintain authentic readiness.
          </span>
        </div>
        <div className="flex items-center gap-4 text-[11px]">
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-slate-400"></span>
            <span className="text-slate-400">Self-Reported</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-teal-400 shadow-sm shadow-teal-400/50"></span>
            <span className="text-teal-300 font-semibold">Verified Test Score</span>
          </div>
        </div>
      </div>

      {/* Search & Filter Bar */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
          <input
            type="text"
            placeholder="Search skills by name (e.g. Java, React, SQL)..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-white text-xs outline-none focus:border-cyan-500 transition"
          />
        </div>

        <div className="flex items-center gap-1 overflow-x-auto pb-2 sm:pb-0 scrollbar-none">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition ${
                selectedCategory === cat
                  ? 'bg-cyan-500 text-slate-950 font-bold'
                  : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Skills Grid */}
      {filteredSkills.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredSkills.map((s) => (
            <div
              key={s.id}
              className="p-5 rounded-2xl bg-slate-900 border border-slate-800 hover:border-slate-700 transition flex flex-col justify-between"
            >
              <div>
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <h3 className="font-bold text-white text-base">{s.skill.name}</h3>
                    <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-950 border border-slate-800 text-slate-400 font-mono mt-1 inline-block">
                      {s.skill.category}
                    </span>
                  </div>
                  <button
                    onClick={() => handleDeleteSkill(s.id)}
                    className="text-slate-500 hover:text-red-400 p-1"
                    title="Remove Skill"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>

                {s.skill.description && (
                  <p className="text-xs text-slate-400 mt-2 line-clamp-2">{s.skill.description}</p>
                )}
              </div>

              {/* Status Indicators */}
              <div className="mt-5 pt-3 border-t border-slate-800/80 space-y-2">
                {/* Self-reported level */}
                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-400">Self-Reported Level:</span>
                  <select
                    value={s.self_reported_level}
                    onChange={(e) => handleUpdateLevel(s.id, e.target.value)}
                    className="px-2 py-1 rounded-lg bg-slate-950 border border-slate-700 text-xs text-cyan-300 font-semibold outline-none focus:border-cyan-500"
                  >
                    <option value="Beginner">Beginner</option>
                    <option value="Intermediate">Intermediate</option>
                    <option value="Advanced">Advanced</option>
                  </select>
                </div>

                {/* Verified Assessment Score */}
                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-400">Verified Assessment:</span>
                  {s.assessment_score !== null ? (
                    <span className="inline-flex items-center gap-1 text-teal-400 font-bold font-mono">
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      <span>{s.assessment_score.toFixed(0)}% Score</span>
                    </span>
                  ) : (
                    <span className="text-[11px] text-slate-500 italic">Not tested yet</span>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="p-12 rounded-2xl bg-slate-900 border border-dashed border-slate-800 text-center">
          <Award className="w-10 h-10 text-slate-600 mx-auto mb-3" />
          <h3 className="text-base font-bold text-white">No Skills Found</h3>
          <p className="text-xs text-slate-400 mt-1 max-w-sm mx-auto">
            {searchQuery
              ? 'No skills matching your search query. Try another search or add a custom skill.'
              : 'You have not added any skills to this category yet. Click Add Skill above.'}
          </p>
        </div>
      )}

      {/* Add Skill Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm">
          <div className="w-full max-w-md rounded-2xl bg-slate-900 border border-slate-800 p-6 shadow-2xl">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <h3 className="font-bold text-lg text-white">Add Skill to Inventory</h3>
              <button onClick={() => setShowAddModal(false)} className="text-slate-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleAddSkill} className="mt-4 space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">
                  Select Skill from Catalog
                </label>
                <select
                  value={selectedSkillName}
                  onChange={(e) => setSelectedSkillName(e.target.value)}
                  className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm outline-none focus:border-cyan-500"
                >
                  <option value="">-- Choose from standard catalog --</option>
                  {catalog.map((c) => (
                    <option key={c.id} value={c.name}>
                      {c.name} ({c.category})
                    </option>
                  ))}
                  <option value="custom">+ Enter custom skill name</option>
                </select>
              </div>

              {selectedSkillName === 'custom' && (
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">
                    Custom Skill Name
                  </label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Next.js, GraphQL, Redis"
                    value={customSkillName}
                    onChange={(e) => setCustomSkillName(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm outline-none focus:border-cyan-500"
                  />
                </div>
              )}

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">
                  Self-Reported Proficiency Level
                </label>
                <select
                  value={skillLevel}
                  onChange={(e) => setSkillLevel(e.target.value)}
                  className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm outline-none focus:border-cyan-500"
                >
                  <option value="Beginner">Beginner (Basic understanding of concepts)</option>
                  <option value="Intermediate">Intermediate (Can implement features independently)</option>
                  <option value="Advanced">Advanced (Production experience, architecture & optimization)</option>
                </select>
              </div>

              <div className="pt-2 flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 rounded-xl bg-slate-800 text-slate-300 text-xs font-semibold hover:bg-slate-700"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs"
                >
                  Add Skill
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
