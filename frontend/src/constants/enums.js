/**
 * Application enums and constants
 */

// User types
export const USER_TYPES = {
  PATIENT: 'patient',
  DOCTOR: 'doctor',
  ADMIN: 'admin',
};

// Treatment status
export const TREATMENT_STATUS = {
  ACTIVE: 'active',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled',
  PENDING: 'pending',
};

// Appointment status
export const APPOINTMENT_STATUS = {
  SCHEDULED: 'scheduled',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled',
  MISSED: 'missed',
};

// Blood groups
export const BLOOD_GROUPS = [
  { value: 'A+', label: 'A+' },
  { value: 'A-', label: 'A-' },
  { value: 'B+', label: 'B+' },
  { value: 'B-', label: 'B-' },
  { value: 'AB+', label: 'AB+' },
  { value: 'AB-', label: 'AB-' },
  { value: 'O+', label: 'O+' },
  { value: 'O-', label: 'O-' },
];

// Side effect severity
export const SIDE_EFFECT_SEVERITY = {
  MILD: 1,
  MODERATE: 2,
  SEVERE: 3,
};

// Common side effects
export const COMMON_SIDE_EFFECTS = [
  'Nausea',
  'Headache',
  'Dizziness',
  'Fatigue',
  'Rash',
  'Stomach pain',
  'Drowsiness',
  'Insomnia',
  'Dry mouth',
  'Constipation',
  'Diarrhea',
  'Increased heart rate',
  'Decreased appetite',
  'Anxiety',
  'Blurred vision',
];

// Medication frequencies
export const MEDICATION_FREQUENCIES = [
  { value: 'once_daily', label: 'Once daily' },
  { value: 'twice_daily', label: 'Twice daily' },
  { value: 'three_times_daily', label: 'Three times daily' },
  { value: 'four_times_daily', label: 'Four times daily' },
  { value: 'every_other_day', label: 'Every other day' },
  { value: 'weekly', label: 'Weekly' },
  { value: 'as_needed', label: 'As needed (PRN)' },
];

// Routes of administration
export const ADMINISTRATION_ROUTES = [
  { value: 'oral', label: 'Oral' },
  { value: 'topical', label: 'Topical' },
  { value: 'injection', label: 'Injection' },
  { value: 'inhalation', label: 'Inhalation' },
  { value: 'rectal', label: 'Rectal' },
  { value: 'vaginal', label: 'Vaginal' },
  { value: 'ophthalmic', label: 'Ophthalmic (eye)' },
  { value: 'otic', label: 'Otic (ear)' },
  { value: 'nasal', label: 'Nasal' },
  { value: 'sublingual', label: 'Sublingual' },
];
