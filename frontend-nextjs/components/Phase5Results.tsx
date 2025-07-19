'use client';

import React from 'react';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Download, Video, Mic, Music, FileText, Play, RefreshCw, CheckCircle } from 'lucide-react';
import { motion } from 'framer-motion';
import { FinalVideoResponse, formatBytes, formatDuration } from '@/lib/api';
import toast from 'react-hot-toast';

interface Phase5ResultsProps {
  result: FinalVideoResponse;
  onStartNew: () => void;
}

export function Phase5Results({ result, onStartNew }: Phase5ResultsProps) {
  const script = result.story_script;

  const downloadFile = async (filePath: string, filename: string) => {
    try {
      // Extract file type and name from the path
      const pathParts = filePath.split('/');
      const fileType = pathParts[pathParts.length - 2]; // e.g., 'videos', 'audio', 'music'
      const actualFilename = pathParts[pathParts.length - 1]; // actual filename
      
      // Construct the download URL
      const downloadUrl = `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/files/${fileType}/${actualFilename}`;
      
      // Create a temporary link and trigger download
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = filename;
      link.target = '_blank';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      toast.success(`Downloading ${filename}...`);
    } catch (error) {
      console.error('Download error:', error);
      toast.error(`Failed to download ${filename}`);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="w-full max-w-6xl mx-auto space-y-6"
    >
      {/* Header */}
      <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
        <CardHeader className="text-center">
          <div className="flex justify-center mb-4">
            <div className="w-16 h-16 bg-gradient-to-r from-green-500 to-emerald-600 rounded-full flex items-center justify-center">
              <CheckCircle className="w-8 h-8 text-white" />
            </div>
          </div>
          <CardTitle className="text-3xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
            Your Video is Ready!
          </CardTitle>
          <CardDescription className="text-lg text-gray-600">
            Congratulations! Your story has been transformed into a professional video with all assets ready for download.
          </CardDescription>
        </CardHeader>
      </Card>

      {/* Story Script */}
      <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2 text-xl">
            <FileText className="w-6 h-6 text-blue-600" />
            <span>Story Script</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-4 bg-blue-50 rounded-lg">
                  <h4 className="font-medium text-blue-800">Title</h4>
                  <p className="text-blue-600">{script.story_title}</p>
                </div>
                <div className="p-4 bg-green-50 rounded-lg">
                  <h4 className="font-medium text-green-800">Duration</h4>
                  <p className="text-green-600">{formatDuration(script.total_duration)}</p>
                </div>
                <div className="p-4 bg-purple-50 rounded-lg">
                  <h4 className="font-medium text-purple-800">Scenes</h4>
                  <p className="text-purple-600">{script.scenes.length} scenes</p>
                </div>
              </div>

              <div className="space-y-3">
                <h4 className="font-medium text-gray-900">Scene Breakdown</h4>
                <div className="space-y-2">
                  {script.scenes.map((scene, index) => (
                    <div key={index} className="p-3 bg-gray-50 rounded-lg">
                      <div className="flex items-center justify-between">
                        <span className="font-medium text-gray-900">
                          Scene {index + 1}: {scene.description}
                        </span>
                        <span className="text-sm text-gray-500">{scene.duration}s</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <h4 className="font-medium text-gray-900">Generation Details</h4>
              <div className="space-y-3">
                <div className="p-3 bg-gray-50 rounded-lg">
                  <span className="text-sm font-medium text-gray-700">Image Style</span>
                  <p className="text-gray-900">{script.generation_metadata.image_style}</p>
                </div>
                <div className="p-3 bg-gray-50 rounded-lg">
                  <span className="text-sm font-medium text-gray-700">Voice ID</span>
                  <p className="text-gray-900">{script.generation_metadata.voice_id}</p>
                </div>
                <div className="p-3 bg-gray-50 rounded-lg">
                  <span className="text-sm font-medium text-gray-700">Music Style</span>
                  <p className="text-gray-900">{script.generation_metadata.music_style}</p>
                </div>
                <div className="p-3 bg-gray-50 rounded-lg">
                  <span className="text-sm font-medium text-gray-700">Music Mood</span>
                  <p className="text-gray-900">{script.generation_metadata.music_mood}</p>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Download Files */}
      <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
        <CardHeader>
          <CardTitle className="text-lg">Download Your Files</CardTitle>
          <CardDescription>
            All your generated assets are ready for download. Click on any file to download it.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {/* Video File */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: 0.1 }}
              className="p-4 bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg border border-blue-200 hover:border-blue-300 transition-colors"
            >
              <div className="flex items-center space-x-3 mb-3">
                <Video className="w-6 h-6 text-blue-600" />
                <h4 className="font-medium text-blue-800">Final Video</h4>
              </div>
              <p className="text-sm text-blue-700 mb-3">Complete video with all elements</p>
              <div className="text-xs text-blue-600 mb-3">
                Size: {formatBytes(result.file_sizes.video || 0)}
              </div>
              <Button
                onClick={() => downloadFile(result.video_file, `${script.story_title}.mp4`)}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white"
                size="sm"
              >
                <Download className="w-4 h-4 mr-2" />
                Download
              </Button>
            </motion.div>

            {/* Audio File */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: 0.2 }}
              className="p-4 bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg border border-purple-200 hover:border-purple-300 transition-colors"
            >
              <div className="flex items-center space-x-3 mb-3">
                <Mic className="w-6 h-6 text-purple-600" />
                <h4 className="font-medium text-purple-800">Voice Narration</h4>
              </div>
              <p className="text-sm text-purple-700 mb-3">Professional voice-over</p>
              <div className="text-xs text-purple-600 mb-3">
                Size: {formatBytes(result.file_sizes.audio || 0)}
              </div>
              <Button
                onClick={() => downloadFile(result.audio_file, `${script.story_title}_narration.mp3`)}
                className="w-full bg-purple-600 hover:bg-purple-700 text-white"
                size="sm"
              >
                <Download className="w-4 h-4 mr-2" />
                Download
              </Button>
            </motion.div>

            {/* Music File */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: 0.3 }}
              className="p-4 bg-gradient-to-br from-orange-50 to-orange-100 rounded-lg border border-orange-200 hover:border-orange-300 transition-colors"
            >
              <div className="flex items-center space-x-3 mb-3">
                <Music className="w-6 h-6 text-orange-600" />
                <h4 className="font-medium text-orange-800">Background Music</h4>
              </div>
              <p className="text-sm text-orange-700 mb-3">Mood-matched music</p>
              <div className="text-xs text-orange-600 mb-3">
                Size: {formatBytes(result.file_sizes.music || 0)}
              </div>
              <Button
                onClick={() => downloadFile(result.music_file, `${script.story_title}_music.mp3`)}
                className="w-full bg-orange-600 hover:bg-orange-700 text-white"
                size="sm"
              >
                <Download className="w-4 h-4 mr-2" />
                Download
              </Button>
            </motion.div>

            {/* Images */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: 0.4 }}
              className="p-4 bg-gradient-to-br from-green-50 to-green-100 rounded-lg border border-green-200 hover:border-green-300 transition-colors"
            >
              <div className="flex items-center space-x-3 mb-3">
                <FileText className="w-6 h-6 text-green-600" />
                <h4 className="font-medium text-green-800">Scene Images</h4>
              </div>
              <p className="text-sm text-green-700 mb-3">{result.image_files.length} AI-generated images</p>
              <div className="text-xs text-green-600 mb-3">
                High quality, 1024x1024
              </div>
              <Button
                onClick={() => {
                  result.image_files.forEach((image, index) => {
                    downloadFile(image, `${script.story_title}_scene_${index + 1}.png`);
                  });
                }}
                className="w-full bg-green-600 hover:bg-green-700 text-white"
                size="sm"
              >
                <Download className="w-4 h-4 mr-2" />
                Download All
              </Button>
            </motion.div>
          </div>
        </CardContent>
      </Card>

      {/* Statistics */}
      <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
        <CardHeader>
          <CardTitle className="text-lg">Generation Statistics</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">{formatDuration(result.total_processing_time)}</div>
              <div className="text-sm text-blue-800">Total Time</div>
            </div>
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <div className="text-2xl font-bold text-green-600">{result.image_files.length}</div>
              <div className="text-sm text-green-800">Images Generated</div>
            </div>
            <div className="text-center p-4 bg-purple-50 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">{formatBytes(Object.values(result.file_sizes).reduce((a, b) => a + b, 0))}</div>
              <div className="text-sm text-purple-800">Total Size</div>
            </div>
            <div className="text-center p-4 bg-orange-50 rounded-lg">
              <div className="text-2xl font-bold text-orange-600">{script.scenes.length}</div>
              <div className="text-sm text-orange-800">Scenes Created</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Action Buttons */}
      <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
        <CardContent className="pt-6">
          <div className="flex justify-center">
            <Button
              onClick={onStartNew}
              className="px-8 py-3 text-lg font-medium bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white rounded-lg shadow-lg hover:shadow-xl transition-all duration-200"
            >
              <RefreshCw className="w-5 h-5 mr-2" />
              Create Another Video
            </Button>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
} 