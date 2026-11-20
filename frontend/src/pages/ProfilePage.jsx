import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import {
  User,
  GraduationCap,
  BookOpen,
  Calendar,
  Target,
  Plus,
  Trash2,
  ExternalLink,
  GitBranch,
  CheckCircle2,
  Award,
  FolderKanban,
  Edit2,
  Save,
  X,
  AlertCircle
} from 'lucide-react';

export default function ProfilePage() {
  const { user, refreshUser } = useAuth();
  const [profileData, setProfileData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Editing state for basic info
  const [isEditingBasic, setIsEditingBasic] = useState(false);
  const [basicForm, setBasicForm] = useState({
    name: '',
    college: '',
    degree: '',
    semester: '',
    graduation_year: '',
    career_interest: ''
  });

  // Modal / Form state for new Project
  const [showProjectModal, setShowProjectModal] = useState(false);
  const [projectForm, setProjectForm] = useState({
    title: '',
    description: '',
    technologies: '',
    github_url: '',
    live_url: '',
    status: 'In Progress'
  });

  // Modal / Form state for new Certification
  const [showCertModal, setShowCertModal] = useState(false);
  const [certForm, setCertForm] = useState({
    title: '',
    issuing_organization: '',
    completion_date: '',
    credential_url: ''
  });

  const fetchProfile = async () => {
    try {
      setLoading(true);
      const res = await api.get('/profile');
      setProfileData(res.data);
      setBasicForm({
        name: res.data.user.name || '',
        college: res.data.basic_info.college || '',
        degree: res.data.basic_info.degree || '',
        semester: res.data.basic_info.semester || '',
        graduation_year: res.data.basic_info.graduation_year || '',
        career_interest: res.data.target_role || ''
      });
    } catch (err) {
      console.error(err);
      setError('Failed to load student profile.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfile();
  }, []);

  const handleSaveBasic = async (e) => {
    e.preventDefault();
    try {
      setError('');
      await api.put('/profile', {
        name: basicForm.name,
        college: basicForm.college,
        degree: basicForm.degree,
        semester: basicForm.semester,
        graduation_year: basicForm.graduation_year ? parseInt(basicForm.graduation_year) : null,
        career_interest: basicForm.career_interest
      });

      // Also update career goal if changed
      if (basicForm.career_interest) {
        await api.post('/profile/career-goals', {
          target_role: basicForm.career_interest
        });
      }

      setSuccess('Profile updated successfully.');
      setIsEditingBasic(false);
      await fetchProfile();
      await refreshUser();
      setTimeout(() => setSuccess(''), 4000);
    } catch (err) {
      setError('Failed to update basic profile.');
    }
  };

  const handleCreateProject = async (e) => {
    e.preventDefault();
    try {
      await api.post('/profile/projects', projectForm);
      setShowProjectModal(false);
      setProjectForm({
        title: '',
        description: '',
        technologies: '',
        github_url: '',
        live_url: '',
        status: 'In Progress'
      });
      setSuccess('Project added to portfolio.');
      fetchProfile();
      setTimeout(() => setSuccess(''), 4000);
    } catch (err) {
      setError('Failed to add project.');
    }
  };

  const handleDeleteProject = async (id) => {
    if (!window.confirm('Are you sure you want to delete this project?')) return;
    try {
      await api.delete(`/profile/projects/${id}`);
      fetchProfile();
    } catch (err) {
      setError('Failed to delete project.');
    }
  };

  const handleCreateCert = async (e) => {
    e.preventDefault();
    try {
      await api.post('/profile/certifications', certForm);
      setShowCertModal(false);
      setCertForm({
        title: '',
        issuing_organization: '',
        completion_date: '',
        credential_url: ''
      });
      setSuccess('Certification added to profile.');
      fetchProfile();
      setTimeout(() => setSuccess(''), 4000);
    } catch (err) {
      setError('Failed to add certification.');
    }
  };

  const handleDeleteCert = async (id) => {
    if (!window.confirm('Delete this certification?')) return;
    try {
      await api.delete(`/profile/certifications/${id}`);
      fetchProfile();
    } catch (err) {
      setError('Failed to delete certification.');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="w-10 h-10 border-4 border-cyan-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-12">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Unified Student Capability Profile
          </h1>
          <p className="mt-1 text-sm text-slate-400">
            Comprehensive portfolio of academic background, skills, certifications, and projects
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

      {/* Basic Academic Information */}
      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow">
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400 font-bold">
              <User className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white">Basic Information & Academic Credentials</h2>
              <p className="text-xs text-slate-400">University, degree, current standing, and career interest</p>
            </div>
          </div>
          <button
            onClick={() => setIsEditingBasic(!isEditingBasic)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold transition"
          >
            {isEditingBasic ? <X className="w-3.5 h-3.5" /> : <Edit2 className="w-3.5 h-3.5" />}
            <span>{isEditingBasic ? 'Cancel' : 'Edit Info'}</span>
          </button>
        </div>

        {isEditingBasic ? (
          <form onSubmit={handleSaveBasic} className="mt-6 space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Full Name</label>
                <input
                  type="text"
                  required
                  value={basicForm.name}
                  onChange={(e) => setBasicForm({ ...basicForm, name: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm outline-none focus:border-cyan-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">College / University</label>
                <input
                  type="text"
                  required
                  value={basicForm.college}
                  onChange={(e) => setBasicForm({ ...basicForm, college: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm outline-none focus:border-cyan-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Degree / Course</label>
                <input
                  type="text"
                  required
                  value={basicForm.degree}
                  onChange={(e) => setBasicForm({ ...basicForm, degree: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm outline-none focus:border-cyan-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Semester / Standing</label>
                <input
                  type="text"
                  value={basicForm.semester}
                  onChange={(e) => setBasicForm({ ...basicForm, semester: e.target.value })}
                  placeholder="e.g. 6th Semester"
                  className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm outline-none focus:border-cyan-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Graduation Year</label>
                <input
                  type="number"
                  value={basicForm.graduation_year}
                  onChange={(e) => setBasicForm({ ...basicForm, graduation_year: e.target.value })}
                  placeholder="e.g. 2026"
                  className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm outline-none focus:border-cyan-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Target Career Goal</label>
                <select
                  value={basicForm.career_interest}
                  onChange={(e) => setBasicForm({ ...basicForm, career_interest: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm outline-none focus:border-cyan-500"
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

            <button
              type="submit"
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs shadow transition"
            >
              <Save className="w-4 h-4" />
              <span>Save Changes</span>
            </button>
          </form>
        ) : (
          <div className="mt-6 grid grid-cols-2 sm:grid-cols-3 gap-6">
            <div>
              <div className="text-xs text-slate-400 font-semibold uppercase">Full Name</div>
              <div className="text-sm font-bold text-white mt-1">{profileData.user.name}</div>
            </div>
            <div>
              <div className="text-xs text-slate-400 font-semibold uppercase">Email</div>
              <div className="text-sm font-medium text-slate-300 mt-1">{profileData.user.email}</div>
            </div>
            <div>
              <div className="text-xs text-slate-400 font-semibold uppercase">College / University</div>
              <div className="text-sm font-medium text-slate-300 mt-1">{profileData.basic_info.college || 'Not set'}</div>
            </div>
            <div>
              <div className="text-xs text-slate-400 font-semibold uppercase">Degree / Course</div>
              <div className="text-sm font-medium text-slate-300 mt-1">{profileData.basic_info.degree || 'Not set'}</div>
            </div>
            <div>
              <div className="text-xs text-slate-400 font-semibold uppercase">Current Semester</div>
              <div className="text-sm font-medium text-slate-300 mt-1">{profileData.basic_info.semester || 'Not set'}</div>
            </div>
            <div>
              <div className="text-xs text-slate-400 font-semibold uppercase">Target Career Role</div>
              <div className="text-sm font-bold text-cyan-400 mt-1">{profileData.target_role || 'Java Developer'}</div>
            </div>
          </div>
        )}
      </div>

      {/* Projects Portfolio Section */}
      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow">
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-teal-500/10 border border-teal-500/20 flex items-center justify-center text-teal-400 font-bold">
              <FolderKanban className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white">Student Projects & Practical Portfolio</h2>
              <p className="text-xs text-slate-400">Real application deliverables demonstrating implementation ability</p>
            </div>
          </div>
          <button
            onClick={() => setShowProjectModal(true)}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-teal-500 hover:bg-teal-400 text-slate-950 font-bold text-xs transition"
          >
            <Plus className="w-4 h-4" />
            <span>Add Project</span>
          </button>
        </div>

        {profileData.projects && profileData.projects.length > 0 ? (
          <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
            {profileData.projects.map((proj) => (
              <div key={proj.id} className="p-4 rounded-xl bg-slate-950 border border-slate-800/80 flex flex-col justify-between">
                <div>
                  <div className="flex items-start justify-between gap-2">
                    <h3 className="font-bold text-white text-base">{proj.title}</h3>
                    <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 font-medium">
                      {proj.status}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 mt-2 line-clamp-2">{proj.description}</p>
                  {proj.technologies && (
                    <div className="mt-3 flex flex-wrap gap-1.5">
                      {proj.technologies.split(',').map((tech, idx) => (
                        <span key={idx} className="text-[10px] px-2 py-0.5 rounded bg-slate-900 border border-slate-700/60 text-slate-300 font-mono">
                          {tech.trim()}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between text-xs">
                  <div className="flex items-center gap-3">
                    {proj.github_url && (
                      <a href={proj.github_url} target="_blank" rel="noreferrer" className="flex items-center gap-1 text-slate-400 hover:text-white">
                        <GitBranch className="w-3.5 h-3.5" />
                        <span>Code</span>
                      </a>
                    )}
                    {proj.live_url && (
                      <a href={proj.live_url} target="_blank" rel="noreferrer" className="flex items-center gap-1 text-cyan-400 hover:text-cyan-300">
                        <ExternalLink className="w-3.5 h-3.5" />
                        <span>Live Demo</span>
                      </a>
                    )}
                  </div>
                  <button
                    onClick={() => handleDeleteProject(proj.id)}
                    className="text-slate-500 hover:text-red-400 p-1"
                    title="Delete Project"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="mt-6 p-8 rounded-xl bg-slate-950/40 border border-dashed border-slate-800 text-center">
            <FolderKanban className="w-8 h-8 text-slate-600 mx-auto mb-2" />
            <p className="text-xs text-slate-400">No projects added yet.</p>
            <button
              onClick={() => setShowProjectModal(true)}
              className="mt-3 text-xs font-semibold text-teal-400 hover:text-teal-300"
            >
              + Add your first project or adopt one from Project Hub
            </button>
          </div>
        )}
      </div>

      {/* Certifications Section */}
      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow">
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 font-bold">
              <Award className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white">Certifications & Credentials</h2>
              <p className="text-xs text-slate-400">Verified course certificates and industry credentials</p>
            </div>
          </div>
          <button
            onClick={() => setShowCertModal(true)}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-indigo-500 hover:bg-indigo-400 text-white font-bold text-xs transition"
          >
            <Plus className="w-4 h-4" />
            <span>Add Certificate</span>
          </button>
        </div>

        {profileData.certifications && profileData.certifications.length > 0 ? (
          <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 gap-4">
            {profileData.certifications.map((c) => (
              <div key={c.id} className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex items-start justify-between">
                <div>
                  <h3 className="font-bold text-white text-sm">{c.title}</h3>
                  <p className="text-xs text-slate-400 mt-0.5">{c.issuing_organization}</p>
                  {c.completion_date && (
                    <p className="text-[10px] text-slate-400 mt-1 font-mono">Completed: {c.completion_date}</p>
                  )}
                  {c.credential_url && (
                    <a href={c.credential_url} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1 text-[11px] text-indigo-400 hover:text-indigo-300 mt-2">
                      <ExternalLink className="w-3 h-3" />
                      <span>View Credential</span>
                    </a>
                  )}
                </div>
                <button
                  onClick={() => handleDeleteCert(c.id)}
                  className="text-slate-500 hover:text-red-400 p-1"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            ))}
          </div>
        ) : (
          <div className="mt-6 p-8 rounded-xl bg-slate-950/40 border border-dashed border-slate-800 text-center">
            <Award className="w-8 h-8 text-slate-600 mx-auto mb-2" />
            <p className="text-xs text-slate-400">No certifications added yet.</p>
          </div>
        )}
      </div>

      {/* New Project Modal */}
      {showProjectModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm">
          <div className="w-full max-w-lg rounded-2xl bg-slate-900 border border-slate-800 p-6 shadow-2xl">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <h3 className="font-bold text-lg text-white">Add Project to Portfolio</h3>
              <button onClick={() => setShowProjectModal(false)} className="text-slate-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleCreateProject} className="mt-4 space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Project Title</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Enterprise Employee Management System"
                  value={projectForm.title}
                  onChange={(e) => setProjectForm({ ...projectForm, title: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm outline-none focus:border-teal-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Description</label>
                <textarea
                  rows={3}
                  placeholder="Overview of the application, architecture, and what problem it solves..."
                  value={projectForm.description}
                  onChange={(e) => setProjectForm({ ...projectForm, description: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm outline-none focus:border-teal-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Technologies (comma-separated)</label>
                <input
                  type="text"
                  placeholder="Java, Spring Boot, PostgreSQL, React"
                  value={projectForm.technologies}
                  onChange={(e) => setProjectForm({ ...projectForm, technologies: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm outline-none focus:border-teal-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">GitHub URL</label>
                  <input
                    type="url"
                    placeholder="https://github.com/..."
                    value={projectForm.github_url}
                    onChange={(e) => setProjectForm({ ...projectForm, github_url: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm outline-none focus:border-teal-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Live Demo URL</label>
                  <input
                    type="url"
                    placeholder="https://my-app.vercel.app"
                    value={projectForm.live_url}
                    onChange={(e) => setProjectForm({ ...projectForm, live_url: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm outline-none focus:border-teal-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Status</label>
                <select
                  value={projectForm.status}
                  onChange={(e) => setProjectForm({ ...projectForm, status: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm outline-none focus:border-teal-500"
                >
                  <option value="Planned">Planned</option>
                  <option value="In Progress">In Progress</option>
                  <option value="Completed">Completed</option>
                </select>
              </div>

              <div className="pt-2 flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setShowProjectModal(false)}
                  className="px-4 py-2 rounded-xl bg-slate-800 text-slate-300 text-xs font-semibold hover:bg-slate-700"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-xl bg-teal-500 hover:bg-teal-400 text-slate-950 font-bold text-xs"
                >
                  Save Project
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* New Certification Modal */}
      {showCertModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm">
          <div className="w-full max-w-md rounded-2xl bg-slate-900 border border-slate-800 p-6 shadow-2xl">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <h3 className="font-bold text-lg text-white">Add Certification</h3>
              <button onClick={() => setShowCertModal(false)} className="text-slate-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleCreateCert} className="mt-4 space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Certificate Title</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. AWS Certified Developer"
                  value={certForm.title}
                  onChange={(e) => setCertForm({ ...certForm, title: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Issuing Organization</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Amazon Web Services / Coursera"
                  value={certForm.issuing_organization}
                  onChange={(e) => setCertForm({ ...certForm, issuing_organization: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Completion Date</label>
                <input
                  type="text"
                  placeholder="e.g. Nov 2026"
                  value={certForm.completion_date}
                  onChange={(e) => setCertForm({ ...certForm, completion_date: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Credential URL</label>
                <input
                  type="url"
                  placeholder="https://..."
                  value={certForm.credential_url}
                  onChange={(e) => setCertForm({ ...certForm, credential_url: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm outline-none focus:border-indigo-500"
                />
              </div>

              <div className="pt-2 flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setShowCertModal(false)}
                  className="px-4 py-2 rounded-xl bg-slate-800 text-slate-300 text-xs font-semibold hover:bg-slate-700"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-xl bg-indigo-500 hover:bg-indigo-400 text-white font-bold text-xs"
                >
                  Save Certificate
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
