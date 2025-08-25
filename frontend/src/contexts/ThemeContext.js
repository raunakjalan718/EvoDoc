import React, { createContext, useState, useContext, useEffect } from 'react';

// Create the context
const ThemeContext = createContext();

// Available themes
const themes = {
  light: {
    name: 'light',
    background: '#ffffff',
    text: '#333333',
    primary: '#C53030',
    secondary: '#718096',
    card: '#ffffff',
  },
  dark: {
    name: 'dark',
    background: '#1A202C',
    text: '#E2E8F0',
    primary: '#F56565',
    secondary: '#A0AEC0',
    card: '#2D3748',
  },
};

// Theme provider component
export const ThemeProvider = ({ children }) => {
  // Check local storage for saved theme or use system preference
  const getSavedTheme = () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme && themes[savedTheme]) {
      return savedTheme;
    }
    
    // Check for system preference
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }
    
    return 'light';
  };
  
  const [currentTheme, setCurrentTheme] = useState(getSavedTheme);
  
  // Update when system preference changes
  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    const handleChange = () => {
      // Only update if user hasn't explicitly chosen a theme
      if (!localStorage.getItem('theme')) {
        setCurrentTheme(mediaQuery.matches ? 'dark' : 'light');
      }
    };
    
    // Add listener for theme changes
    if (mediaQuery.addEventListener) {
      mediaQuery.addEventListener('change', handleChange);
    } else {
      // Older browsers support
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
  }, []);
  
  // Update theme in local storage when it changes
  useEffect(() => {
    localStorage.setItem('theme', currentTheme);
    
    // Update CSS variables or class on body
    document.body.className = currentTheme === 'dark' ? 'dark-theme' : 'light-theme';
    
  }, [currentTheme]);
  
  // Toggle between light and dark themes
  const toggleTheme = () => {
    setCurrentTheme(prevTheme => prevTheme === 'light' ? 'dark' : 'light');
  };
  
  // Set a specific theme
  const setTheme = (themeName) => {
    if (themes[themeName]) {
      setCurrentTheme(themeName);
    }
  };
  
  return (
    <ThemeContext.Provider 
      value={{ 
        theme: themes[currentTheme], 
        toggleTheme,
        setTheme,
        isDark: currentTheme === 'dark'
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
};

// Custom hook to use the theme context
export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};
