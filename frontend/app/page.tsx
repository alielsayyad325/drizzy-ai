'use client';

import { useState } from 'react';
import SongGenerator from '@/components/SongGenerator';
import AudioPlayer from '@/components/AudioPlayer';

export default function Home() {
  const [generatedSong, setGeneratedSong] = useState<any>(null);

  return (
    <main className="min-h-screen bg-gradient-to-br from-purple-900 via-black to-indigo-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-6xl font-bold bg-gradient-to-r from-purple-400 to-pink-600 bg-clip-text text-transparent mb-4">
            Drizzy AI
          </h1>
          <p className="text-gray-300 text-xl">
            Generate Original Hip-Hop Songs with AI
          </p>
        </header>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-7xl mx-auto">
          {/* Song Generator */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
            <h2 className="text-2xl font-bold text-white mb-6">Create Your Song</h2>
            <SongGenerator onSongGenerated={setGeneratedSong} />
          </div>

          {/* Audio Player & Results */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
            <h2 className="text-2xl font-bold text-white mb-6">Your Song</h2>
            {generatedSong ? (
              <AudioPlayer song={generatedSong} />
            ) : (
              <div className="flex items-center justify-center h-64 text-gray-400">
                <p>Your generated song will appear here</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
