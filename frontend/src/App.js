import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Chat from './components/Chat';
import { createSession, getStatus } from './services/api';

function App() {
  const [sessionId, setSessionId] = useState(null);
  const [status, setStatus] = useState({
    isLoading: true,
    isOnline: false,
    articlesCount: 0,
  });

  // Initialize session on component mount
  useEffect(() => {
    const initializeSession = async () => {
      try {
        // Get system status
        const statusData = await getStatus();
        setStatus({
          isLoading: false,
          isOnline: statusData.status === 'online',
          articlesCount: statusData.articles_count,
        });

        // Create new session
        const { session_id } = await createSession();
        setSessionId(session_id);
        console.log('Session created:', session_id);
      } catch (error) {
        console.error('Error initializing session:', error);
        setStatus({
          isLoading: false,
          isOnline: false,
          articlesCount: 0,
        });
      }
    };

    initializeSession();
  }, []);

  // Handle clearing session and creating a new one
  const handleResetSession = async () => {
    try {
      const { session_id } = await createSession();
      setSessionId(session_id);
      console.log('Session reset, new session:', session_id);
    } catch (error) {
      console.error('Error resetting session:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header 
        status={status}
        onResetSession={handleResetSession}
      />
      
      <main className="container mx-auto px-4 py-6">
        {status.isLoading ? (
          <div className="flex justify-center items-center h-96">
            <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-primary-600"></div>
          </div>
        ) : status.isOnline ? (
          sessionId ? (
            <Chat 
              sessionId={sessionId} 
              onResetSession={handleResetSession}
            />
          ) : (
            <div className="text-center py-10">
              <p className="text-red-500">Failed to create session</p>
              <button 
                onClick={handleResetSession}
                className="mt-4 px-4 py-2 bg-primary-600 text-white rounded hover:bg-primary-700"
              >
                Retry
              </button>
            </div>
          )
        ) : (
          <div className="text-center py-10">
            <p className="text-red-500">System is offline</p>
            <button 
              onClick={() => window.location.reload()}
              className="mt-4 px-4 py-2 bg-primary-600 text-white rounded hover:bg-primary-700"
            >
              Refresh
            </button>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;