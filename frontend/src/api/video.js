const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export async function generateSlideshow({ files, durationSeconds = 2, slideEffect = true, transition = 'slide' }) {
  if (!files || files.length < 2 || files.length > 3) {
    throw new Error('Please select 2 to 3 images.');
  }

  // Get token from localStorage - required for authentication
  const token = localStorage.getItem('token');
  if (!token) {
    throw new Error('Authentication required. Please log in.');
  }

  const formData = new FormData();
  for (const f of files) {
    formData.append('images', f);
  }
  formData.append('duration_seconds', String(durationSeconds));
  formData.append('slide_effect', String(slideEffect));
  formData.append('transition', String(transition));

  // Set Authorization header - must be set for FormData requests
  const headers = {
    'Authorization': `Bearer ${token}`
  };
  // Note: Don't set Content-Type - browser will set it automatically with boundary for FormData

  const resp = await fetch(`${API_BASE_URL}/api/video/slideshow`, {
    method: 'POST',
    headers,
    body: formData,
  });

  if (!resp.ok) {
    const err = await resp.json().catch(() => ({}));
    if (resp.status === 401 || resp.status === 403) {
      // Token expired or invalid - clear it and ask user to login
      localStorage.removeItem('token');
      throw new Error('Session expired. Please log in again.');
    }
    throw new Error(err.detail || 'Failed to generate slideshow');
  }
  return await resp.json();
}