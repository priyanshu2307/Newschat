import React from 'react';

function Header({ status, onResetSession }) {
  return (
    <header className="bg-white shadow">
      <div className="container mx-auto px-4 py-6 flex justify-between items-center">
        <div className="flex items-center">
          <h1 className="text-2xl font-bold text-gray-800">NewsChat</h1>
          <div className="ml-4 text-sm">
            <span className="font-medium">Status:</span>{' '}
            {status.isLoading ? (
              <span className="text-yellow-500">Loading...</span>
            ) : status.isOnline ? (
              <span className="text-green-500">Online</span>
            ) : (
              <span className="text-red-500">Offline</span>
            )}
          </div>
          <div className="ml-4 text-sm">
            <span className="font-medium">Articles:</span>{' '}
            <span>{status.articlesCount}</span>
          </div>
        </div>
        
        <button
          onClick={onResetSession}
          className="px-4 py-2 bg-primary-600 text-white rounded hover:bg-primary-700 transition-colors"
        >
          New Chat
        </button>
      </div>
    </header>
  );
}

export default Header;