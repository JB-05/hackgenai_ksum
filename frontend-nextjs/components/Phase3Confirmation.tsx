'use client';

import React from 'react';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Video, Image, Mic, Music, FileText, AlertTriangle, ArrowLeft } from 'lucide-react';
import { motion } from 'framer-motion';
import { EnhancedPromptResponse } from '@/lib/api';

interface Phase3ConfirmationProps {
  enhancedStory: EnhancedPromptResponse;
  onConfirm: () => void;
  onBack: () => void;
}

export function Phase3Confirmation({ enhancedStory, onConfirm, onBack }: Phase3ConfirmationProps) {
  const generationFeatures = [
    {
      icon: Video,
      title: 'Complete Video',
      description: 'Professional video with smooth transitions',
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
    },
    {
      icon: Image,
      title: 'AI-Generated Images',
      description: 'High-quality images for each scene',
      color: 'text-green-600',
      bgColor: 'bg-green-50',
    },
    {
      icon: Mic,
      title: 'Voice Narration',
      description: 'Professional voice-over for your story',
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
    },
    {
      icon: Music,
      title: 'Background Music',
      description: 'Mood-matched music to enhance the story',
      color: 'text-orange-600',
      bgColor: 'bg-orange-50',
    },
    {
      icon: FileText,
      title: 'Story Script',
      description: 'Complete script and scene breakdown',
      color: 'text-indigo-600',
      bgColor: 'bg-indigo-50',
    },
  ];

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
            <div className="w-16 h-16 bg-gradient-to-r from-orange-500 to-red-600 rounded-full flex items-center justify-center">
              <Video className="w-8 h-8 text-white" />
            </div>
          </div>
          <CardTitle className="text-3xl font-bold bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent">
            Confirm Video Generation
          </CardTitle>
          <CardDescription className="text-lg text-gray-600">
            Ready to create your professional video? Review what will be generated and confirm to proceed.
          </CardDescription>
        </CardHeader>
      </Card>

      {/* Story Summary */}
      <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
        <CardHeader>
          <CardTitle className="text-lg">Story Summary</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-blue-50 rounded-lg">
              <h4 className="font-medium text-blue-800">Title</h4>
              <p className="text-blue-600">{enhancedStory.story_title}</p>
            </div>
            <div className="p-4 bg-green-50 rounded-lg">
              <h4 className="font-medium text-green-800">Scenes</h4>
              <p className="text-green-600">{enhancedStory.estimated_scenes} scenes</p>
            </div>
            <div className="p-4 bg-purple-50 rounded-lg">
              <h4 className="font-medium text-purple-800">Duration</h4>
              <p className="text-purple-600">~{enhancedStory.estimated_scenes * 5}s</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* What Will Be Generated */}
      <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
        <CardHeader>
          <CardTitle className="text-lg">What Will Be Generated</CardTitle>
          <CardDescription>
            Your story will be transformed into a complete video with the following elements:
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {generationFeatures.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
                className={`p-4 rounded-lg border ${feature.bgColor}`}
              >
                <div className="flex items-center space-x-3">
                  <feature.icon className={`w-6 h-6 ${feature.color}`} />
                  <div>
                    <h4 className="font-medium text-gray-900">{feature.title}</h4>
                    <p className="text-sm text-gray-600">{feature.description}</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Important Notes */}
      <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm border-yellow-200 bg-yellow-50/50">
        <CardContent className="pt-6">
          <div className="flex items-start space-x-3">
            <AlertTriangle className="w-6 h-6 text-yellow-600 mt-0.5 flex-shrink-0" />
            <div className="space-y-2">
              <h4 className="font-medium text-yellow-800">Important Notes</h4>
              <ul className="text-sm text-yellow-700 space-y-1">
                <li>• This will use AI credits for image generation, voice synthesis, and music creation</li>
                <li>• Generation typically takes 3-5 minutes</li>
                <li>• You'll receive a complete video file and all individual assets</li>
                <li>• All files will be available for download</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Action Buttons */}
      <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
        <CardContent className="pt-6">
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button
              onClick={onBack}
              variant="outline"
              className="px-8 py-3 text-lg font-medium"
            >
              <ArrowLeft className="w-5 h-5 mr-2" />
              Go Back
            </Button>
            <Button
              onClick={onConfirm}
              className="px-8 py-3 text-lg font-medium bg-gradient-to-r from-orange-600 to-red-600 hover:from-orange-700 hover:to-red-700 text-white rounded-lg shadow-lg hover:shadow-xl transition-all duration-200"
            >
              <Video className="w-5 h-5 mr-2" />
              Start Video Generation
            </Button>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
} 