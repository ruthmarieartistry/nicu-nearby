import React, { useState } from 'react';

export default function NICUFinder() {
  const [searchInput, setSearchInput] = useState('');
  const [zipCode, setZipCode] = useState('');
  const [stateInput, setStateInput] = useState('');
  const [radius, setRadius] = useState('60');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [includeDetails, setIncludeDetails] = useState(false);
  const [showHowToUse, setShowHowToUse] = useState(false);
  const [showMethod, setShowMethod] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    setError('');
    setResults([]);
    try {
      let location = '';
      if (zipCode) {
        location = zipCode;
      } else if (searchInput && stateInput) {
        location = searchInput + ', ' + stateInput;
      } else if (searchInput) {
        location = searchInput;
      }
      if (!location) {
        setError('Please enter a city/state or ZIP code');
        setLoading(false);
        return;
      }
  let url = '/api/search-nicus?location=' + encodeURIComponent(location) + '&radius=' + radius;
  if (includeDetails) url += '&includeDetails=1';
      const response = await fetch(url);
      const data = await response.json();
      if (data.error) {
        setError(data.error);
      } else {
        setResults(data.results || []);
      }
    } catch (err) {
      setError('Failed to search. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const rubyRed = '#7d2431';
  const darkGreen = '#217045';
  const mustardYellow = '#e1b321';
  const goldBrown = '#a5630b';
  const darkTeal = '#005567';

  return React.createElement('div', { className: 'min-h-screen bg-gray-50' },
    React.createElement('header', { className: 'bg-white border-b border-gray-200 py-4 px-6' },
      React.createElement('div', { className: 'max-w-7xl mx-auto' })
    ),
    React.createElement('div', { className: 'max-w-7xl mx-auto px-6 py-12' },
      React.createElement('div', { className: 'grid grid-cols-12 gap-8' },
        React.createElement('aside', { className: 'col-span-4 space-y-8' },
          React.createElement('div', { className: 'text-center' },
            React.createElement('p', { className: 'text-xs font-semibold text-gray-400 tracking-widest mb-4' }, 'CREATED FOR'),
            React.createElement('div', { className: 'bg-white rounded-xl p-6 border border-gray-200' },
              React.createElement('img', { src: '/alcea-logo.png', alt: 'ALCEA Logo', className: 'w-full h-auto mb-2' }),
              React.createElement('p', { className: 'text-sm font-medium text-gray-500' }, '2025')
            )
          ),
          React.createElement('div', { className: 'space-y-3' },
            React.createElement('button', {
              onClick: () => setShowHowToUse(true),
              className: 'w-full text-left px-6 py-4 rounded-xl text-white font-semibold flex items-center gap-3 transition-all hover:opacity-90',
              style: { backgroundColor: goldBrown }
            },
              React.createElement('div', { className: 'w-7 h-7 rounded-full border-2 border-white flex items-center justify-center text-lg font-bold flex-shrink-0' }, '?'),
              React.createElement('span', {}, 'How To Use')
            ),
            React.createElement('button', {
              onClick: () => setShowMethod(true),
              className: 'w-full text-left px-6 py-4 rounded-xl text-white font-semibold flex items-center gap-3 transition-all hover:opacity-90',
              style: { backgroundColor: mustardYellow }
            },
              React.createElement('svg', { className: 'w-6 h-6 flex-shrink-0', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' },
                React.createElement('path', { strokeLinecap: 'round', strokeLinejoin: 'round', strokeWidth: 2, d: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' })
              ),
              React.createElement('span', {}, 'Method & Reliability')
            )
          )
        ),
        React.createElement('main', { className: 'col-span-8' },
          React.createElement('div', { className: 'mb-8' },
            React.createElement('img', { src: '/nicunearby-logo.png', alt: 'NICU Nearby', className: 'h-16 w-auto mb-4' }),
            React.createElement('p', { className: 'text-lg text-gray-600' }, 'Search comprehensive, real-time information about NICU facilities across the United States. ')
          ),
          React.createElement('div', { className: 'bg-white rounded-xl shadow-sm border border-gray-200 p-8 mb-8' },
            React.createElement('div', { className: 'flex items-center gap-3 mb-6' },
              React.createElement('div', { className: 'w-12 h-12 rounded-xl flex items-center justify-center', style: { backgroundColor: rubyRed + '20' } },
                React.createElement('svg', { className: 'w-6 h-6', style: { color: rubyRed }, fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' },
                  React.createElement('path', { strokeLinecap: 'round', strokeLinejoin: 'round', strokeWidth: 2, d: 'M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z' }),
                  React.createElement('path', { strokeLinecap: 'round', strokeLinejoin: 'round', strokeWidth: 2, d: 'M15 11a3 3 0 11-6 0 3 3 0 016 0z' })
                )
              ),
              React.createElement('h2', { className: 'text-2xl font-semibold', style: { color: rubyRed } }, 'Search NICU Database')
            ),
            React.createElement('div', { className: 'grid grid-cols-3 gap-6 mb-6' },
              React.createElement('div', {},
                React.createElement('label', { className: 'block text-sm font-medium mb-2', style: { color: darkTeal } }, 'City'),
                React.createElement('input', {
                  type: 'text',
                  value: searchInput,
                  onChange: (e) => setSearchInput(e.target.value),
                  placeholder: 'e.g., New York',
                  className: 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2'
                })
              ),
              React.createElement('div', {},
                React.createElement('label', { className: 'block text-sm font-medium mb-2', style: { color: darkTeal } }, 'State'),
                React.createElement('input', {
                  type: 'text',
                  value: stateInput,
                  onChange: (e) => setStateInput(e.target.value),
                  placeholder: 'e.g., NY',
                  className: 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2'
                })
              ),
              React.createElement('div', {},
                React.createElement('label', { className: 'block text-sm font-medium mb-2', style: { color: darkTeal } }, 'ZIP Code'),
                React.createElement('input', {
                  type: 'text',
                  value: zipCode,
                  onChange: (e) => setZipCode(e.target.value),
                  placeholder: 'e.g., 10001',
                  className: 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2'
                })
              )
            ),
            React.createElement('div', { className: 'mb-6' },
              React.createElement('label', { className: 'block text-sm font-medium mb-2', style: { color: darkTeal } }, 'Search Radius'),
              React.createElement('select', {
                value: radius,
                onChange: (e) => setRadius(e.target.value),
                className: 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2'
              },
                React.createElement('option', { value: '20' }, '20 miles'),
                React.createElement('option', { value: '25' }, '25 miles'),
                React.createElement('option', { value: '40' }, '40 miles'),
                React.createElement('option', { value: '60' }, '60 miles'),
                React.createElement('option', { value: '100' }, '100 miles')
              )
            ),
            React.createElement('div', { className: 'mb-4 flex items-center gap-3' },
              React.createElement('input', {
                id: 'includeDetails',
                type: 'checkbox',
                checked: includeDetails,
                onChange: (e) => setIncludeDetails(e.target.checked),
                className: 'h-4 w-4'
              }),
              React.createElement('label', { htmlFor: 'includeDetails', className: 'text-sm text-gray-700' }, 'Include additional details (phone, website)')
            ),
            React.createElement('button', {
              onClick: handleSearch,
              disabled: loading,
              className: 'w-full py-4 text-white rounded-lg font-semibold text-lg flex items-center justify-center gap-3 transition-all hover:opacity-90 disabled:opacity-50',
              style: { backgroundColor: darkGreen }
            },
              loading ? 
                React.createElement(React.Fragment, {},
                  React.createElement('div', { className: 'w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin' }),
                  'Searching...'
                ) :
                React.createElement(React.Fragment, {},
                  React.createElement('svg', { className: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' },
                    React.createElement('path', { strokeLinecap: 'round', strokeLinejoin: 'round', strokeWidth: 2, d: 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z' })
                  ),
                  'Search Hospitals'
                )
            ),
            error && React.createElement('div', { className: 'mt-4 p-4 rounded-lg bg-red-50 border border-red-200' },
              React.createElement('p', { style: { color: rubyRed } }, error)
            )
          ),
          results.length > 0 && React.createElement('div', { className: 'space-y-4' },
            React.createElement('h2', { className: 'text-2xl font-semibold mb-4', style: { color: darkTeal } },
              'Found ' + results.length + ' NICU facilities within ' + radius + ' miles'
            ),
            results.map((nicu, index) =>
              React.createElement('div', {
                key: index,
                className: 'bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow'
              },
                React.createElement('div', { className: 'flex items-start justify-between mb-3' },
                  React.createElement('h3', { className: 'text-xl font-semibold', style: { color: darkTeal } }, nicu.name),
                  React.createElement('span', {
                    className: 'px-3 py-1 rounded-full text-sm font-medium',
                    style: { backgroundColor: mustardYellow + '20', color: goldBrown }
                  }, nicu.distance + ' miles')
                ),
                React.createElement('p', { className: 'text-gray-600 mb-4' }, nicu.address),
                React.createElement('div', { className: 'flex items-center gap-6 text-sm flex-wrap' },
                  nicu.phone && React.createElement('div', { className: 'flex items-center gap-2 text-gray-600' },
                    React.createElement('svg', { className: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' },
                      React.createElement('path', { strokeLinecap: 'round', strokeLinejoin: 'round', strokeWidth: 2, d: 'M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z' })
                    ),
                    React.createElement('a', { href: 'tel:' + nicu.phone.replace(/[^0-9+]/g, ''), className: 'font-medium text-gray-700 hover:underline' }, nicu.phone)
                  ),
                  nicu.rating && React.createElement('div', { className: 'flex items-center gap-2 text-gray-600' },
                    React.createElement('svg', { className: 'w-4 h-4', style: { color: mustardYellow }, fill: mustardYellow, viewBox: '0 0 20 20' },
                      React.createElement('path', { d: 'M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z' })
                    ),
                    nicu.rating + ' (' + nicu.reviews + ' reviews)'
                  ),
                  nicu.website && React.createElement('a', {
                    href: nicu.website,
                    target: '_blank',
                    rel: 'noopener noreferrer',
                    className: 'flex items-center gap-2 font-medium hover:opacity-80',
                    style: { color: darkTeal }
                  },
                    React.createElement('svg', { className: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' },
                      React.createElement('path', { strokeLinecap: 'round', strokeLinejoin: 'round', strokeWidth: 2, d: 'M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9' })
                    ),
                    'Website'
                  ),
                  nicu.placeId && React.createElement('a', {
                    href: 'https://www.google.com/maps/search/?api=1&query=Google&query_place_id=' + nicu.placeId,
                    target: '_blank',
                    rel: 'noopener noreferrer',
                    className: 'flex items-center gap-2 font-medium hover:opacity-80',
                    style: { color: darkGreen }
                  },
                    React.createElement('svg', { className: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' },
                      React.createElement('path', { strokeLinecap: 'round', strokeLinejoin: 'round', strokeWidth: 2, d: 'M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14' })
                    ),
                    'View on Maps'
                  )
                )
              )
            )
          )
        )
      )
    ),
    showHowToUse && React.createElement('div', {
      className: 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4',
      onClick: () => setShowHowToUse(false)
    },
      React.createElement('div', {
        className: 'bg-white rounded-2xl max-w-2xl w-full max-h-screen overflow-y-auto p-8',
        onClick: (e) => e.stopPropagation()
      },
        React.createElement('div', { className: 'flex items-center justify-between mb-6' },
          React.createElement('h2', { className: 'text-3xl font-bold', style: { color: goldBrown } }, 'How To Use'),
          React.createElement('button', {
            onClick: () => setShowHowToUse(false),
            className: 'text-gray-500 hover:text-gray-700 text-2xl'
          }, '×')
        ),
        React.createElement('div', { className: 'space-y-4 text-gray-700' },
          React.createElement('p', { className: 'text-lg' }, 'Welcome to NICUNearby! Follow these simple steps to find NICU hospitals near you:'),
          React.createElement('div', { className: 'space-y-4' },
            React.createElement('div', { className: 'flex gap-4' },
              React.createElement('div', {
                className: 'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-white font-bold',
                style: { backgroundColor: goldBrown }
              }, '1'),
              React.createElement('div', {},
                React.createElement('h3', { className: 'font-semibold mb-1', style: { color: darkTeal } }, 'Enter Your Location'),
                React.createElement('p', {}, 'Type in your city and state, or simply enter your ZIP code.')
              )
            ),
            React.createElement('div', { className: 'flex gap-4' },
              React.createElement('div', {
                className: 'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-white font-bold',
                style: { backgroundColor: goldBrown }
              }, '2'),
              React.createElement('div', {},
                React.createElement('h3', { className: 'font-semibold mb-1', style: { color: darkTeal } }, 'Select Search Radius'),
                React.createElement('p', {}, 'Choose how far you want to search (20, 40, 60, or 100 miles).')
              )
            ),
            React.createElement('div', { className: 'flex gap-4' },
              React.createElement('div', {
                className: 'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-white font-bold',
                style: { backgroundColor: goldBrown }
              }, '3'),
              React.createElement('div', {},
                React.createElement('h3', { className: 'font-semibold mb-1', style: { color: darkTeal } }, 'Click Search'),
                React.createElement('p', {}, 'Hit the green Search Hospitals button to find nearby NICUs.')
              )
            ),
            React.createElement('div', { className: 'flex gap-4' },
              React.createElement('div', {
                className: 'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-white font-bold',
                style: { backgroundColor: goldBrown }
              }, '4'),
              React.createElement('div', {},
                React.createElement('h3', { className: 'font-semibold mb-1', style: { color: darkTeal } }, 'Review Results'),
                React.createElement('p', {}, 'View hospital details including distance, ratings, and contact information. Click View on Maps to get directions.')
              )
            )
          )
        )
      )
    ),
    showMethod && React.createElement('div', {
      className: 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4',
      onClick: () => setShowMethod(false)
    },
      React.createElement('div', {
        className: 'bg-white rounded-2xl max-w-2xl w-full max-h-screen overflow-y-auto p-8',
        onClick: (e) => e.stopPropagation()
      },
        React.createElement('div', { className: 'flex items-center justify-between mb-6' },
          React.createElement('h2', { className: 'text-3xl font-bold', style: { color: mustardYellow } }, 'Method & Reliability'),
          React.createElement('button', {
            onClick: () => setShowMethod(false),
            className: 'text-gray-500 hover:text-gray-700 text-2xl'
          }, '×')
        ),
        React.createElement('div', { className: 'space-y-4 text-gray-700' },
          React.createElement('p', { className: 'text-lg' }, 'Our NICU search tool uses reliable, up-to-date data to help you find the best care facilities.'),
          React.createElement('div', { className: 'space-y-6' },
            React.createElement('div', {},
              React.createElement('h3', { className: 'font-semibold text-xl mb-2', style: { color: darkTeal } }, 'Data Sources'),
              React.createElement('p', {}, 'We utilize Google Maps Places API to provide comprehensive, real-time information about NICU facilities across the United States.')
            ),
            React.createElement('div', {},
              React.createElement('h3', { className: 'font-semibold text-xl mb-2', style: { color: darkTeal } }, 'Search Methodology'),
              React.createElement('p', {}, 'Our search algorithm identifies hospitals with neonatal intensive care units within your specified radius. We calculate distances based on actual driving routes, not straight-line distances.')
            ),
            React.createElement('div', {},
              React.createElement('h3', { className: 'font-semibold text-xl mb-2', style: { color: darkTeal } }, 'Information Accuracy'),
              React.createElement('p', {}, 'All hospital information including addresses, phone numbers, and ratings are sourced directly from verified databases. We recommend calling ahead to confirm specific NICU services and availability.')
            ),
            React.createElement('div', {},
              React.createElement('h3', { className: 'font-semibold text-xl mb-2', style: { color: darkTeal } }, 'Privacy & Security'),
              React.createElement('p', {}, 'Your search queries are not stored or shared. We are committed to protecting your privacy while providing you with the best possible search experience.')
            )
          )
        )
      )
    )
  );
}