import React from 'react';

export default function Custom404() {
  return React.createElement('div', { className: 'flex items-center justify-center min-h-screen' },
    React.createElement('h1', { className: 'text-4xl font-bold' }, '404 - Page Not Found'),
    React.createElement('p', { className: 'mt-4' }, 'The page you are looking for does not exist.')
  );
}