import { useState, useEffect } from 'react';

/**
 * Custom hook for responsive design with media queries
 * @param {string} query - Media query string
 * @returns {boolean} - Whether the media query matches
 */
const useMediaQuery = (query) => {
  const [matches, setMatches] = useState(false);
  
  useEffect(() => {
    // Create media query list
    const mediaQuery = window.matchMedia(query);
    
    // Set initial value
    setMatches(mediaQuery.matches);
    
    // Define callback for when media query changes
    const handleChange = (event) => {
      setMatches(event.matches);
    };
    
    // Add event listener
    if (mediaQuery.addEventListener) {
      mediaQuery.addEventListener('change', handleChange);
    } else {
      // Fallback for older browsers
      mediaQuery.addListener(handleChange);
    }
    
    // Clean up
    return () => {
      if (mediaQuery.removeEventListener) {
        mediaQuery.removeEventListener('change', handleChange);
      } else {
        mediaQuery.removeListener(handleChange);
      }
    };
  }, [query]);
  
  return matches;
};

// Common breakpoint presets
useMediaQuery.isMobile = () => useMediaQuery('(max-width: 767px)');
useMediaQuery.isTablet = () => useMediaQuery('(min-width: 768px) and (max-width: 1023px)');
useMediaQuery.isDesktop = () => useMediaQuery('(min-width: 1024px)');
useMediaQuery.isLargeDesktop = () => useMediaQuery('(min-width: 1280px)');

export default useMediaQuery;
