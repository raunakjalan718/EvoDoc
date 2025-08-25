import React from 'react';

/**
 * Reusable pagination component
 */
const Pagination = ({
  currentPage,
  totalPages,
  onPageChange,
  className = '',
}) => {
  // If only one page, don't show pagination
  if (totalPages <= 1) return null;
  
  const handlePrevious = () => {
    if (currentPage > 1) {
      onPageChange(currentPage - 1);
    }
  };
  
  const handleNext = () => {
    if (currentPage < totalPages) {
      onPageChange(currentPage + 1);
    }
  };
  
  // Generate array of page numbers to display
  const getPageNumbers = () => {
    const pages = [];
    
    // Always show first and last page
    // For smaller number of pages, show all
    if (totalPages <= 7) {
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i);
      }
    } else {
      // For larger number of pages, show current page and some neighbors
      pages.push(1);
      
      if (currentPage > 3) {
        pages.push('...');
      }
      
      // Show one or two pages before current
      const startPage = Math.max(2, currentPage - 1);
      for (let i = startPage; i < currentPage; i++) {
        pages.push(i);
      }
      
      // Current page
      if (currentPage !== 1 && currentPage !== totalPages) {
        pages.push(currentPage);
      }
      
      // Show one or two pages after current
      const endPage = Math.min(totalPages - 1, currentPage + 1);
      for (let i = currentPage + 1; i <= endPage; i++) {
        pages.push(i);
      }
      
      if (currentPage < totalPages - 2) {
        pages.push('...');
      }
      
      pages.push(totalPages);
    }
    
    return pages;
  };

  return (
    <nav className={`flex items-center justify-between py-3 ${className}`} aria-label="Pagination">
      <div className="flex-1 flex justify-between sm:justify-end">
        <button
          onClick={handlePrevious}
          disabled={currentPage === 1}
          className={`
            relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md
            ${currentPage === 1 
              ? 'bg-gray-100 text-gray-400 cursor-not-allowed' 
              : 'bg-white text-gray-700 hover:bg-gray-50'}
            mr-3
          `}
        >
          Previous
        </button>
        
        <div className="hidden md:flex">
          {getPageNumbers().map((page, index) => (
            <React.Fragment key={index}>
              {page === '...' ? (
                <span className="px-4 py-2 text-gray-700">...</span>
              ) : (
                <button
                  onClick={() => onPageChange(page)}
                  className={`
                    relative inline-flex items-center px-4 py-2 text-sm font-medium
                    ${page === currentPage
                      ? 'bg-primary-100 text-primary-700 border border-primary-500'
                      : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'}
                    ${index > 0 ? '-ml-px' : ''}
                  `}
                  aria-current={page === currentPage ? 'page' : undefined}
                >
                  {page}
                </button>
              )}
            </React.Fragment>
          ))}
        </div>
        
        <button
          onClick={handleNext}
          disabled={currentPage === totalPages}
          className={`
            relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md
            ${currentPage === totalPages
              ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
              : 'bg-white text-gray-700 hover:bg-gray-50'}
            ml-3
          `}
        >
          Next
        </button>
      </div>
    </nav>
  );
};

export default Pagination;
