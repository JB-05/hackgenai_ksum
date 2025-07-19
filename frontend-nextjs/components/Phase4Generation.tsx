'use client';

import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Progress } from '@/components/ui/Progress';
import { Video, Image, Mic, Music, FileText, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';
import { GenerationProgress, workflowAPI } from '@/lib/api';
import toast from 'react-hot-toast';

interface Phase4GenerationProps {
  workflowId: string;
  onComplete: () => void;
  onError: (error: string) => void;
}

export function Phase4Generation({ workflowId, onComplete, onError }: Phase4GenerationProps) {
  const [progress, setProgress] = useState<GenerationProgress | null>(null);
  const [currentStep, setCurrentStep] = useState('Starting generation...');
  const [isGenerating, setIsGenerating] = useState(false);

  const generationSteps = [
    { id: 'scene_breakdown', title: 'Breaking story into scenes', icon: FileText, color: 'text-blue-600' },
    { id: 'image_generation', title: 'Generating images for scenes', icon: Image, color: 'text-green-600' },
    { id: 'voice_synthesis', title: 'Generating voice narration', icon: Mic, color: 'text-purple-600' },
    { id: 'music_generation', title: 'Generating background music', icon: Music, color: 'text-orange-600' },
    { id: 'video_assembly', title: 'Assembling final video', icon: Video, color: 'text-red-600' },
  ];

  useEffect(() => {
    const startGeneration = async () => {
      try {
        setIsGenerating(true);
        
        // Start the generation process
        await workflowAPI.generateVideo(workflowId);
        
        // Start polling for progress
        pollProgress();
        
      } catch (error) {
        console.error('Error starting generation:', error);
        onError('Failed to start generation. Please try again.');
      }
    };

    const pollProgress = async () => {
      try {
        const pollInterval = setInterval(async () => {
          try {
            // Get current progress
            const progressData = await workflowAPI.getProgress(workflowId);
            setProgress(progressData);
            setCurrentStep(progressData.current_step);

            // Check if generation is completed
            if (progressData.status === 'completed') {
              clearInterval(pollInterval);
              setIsGenerating(false);
              setTimeout(() => onComplete(), 1000);
            } else if (progressData.status === 'failed') {
              clearInterval(pollInterval);
              setIsGenerating(false);
              onError('Generation failed. Please try again.');
            }
          } catch (error) {
            console.error('Error polling progress:', error);
            // Continue polling even if there's an error
          }
        }, 2000); // Poll every 2 seconds

        // Cleanup interval on unmount
        return () => clearInterval(pollInterval);
        
      } catch (error) {
        console.error('Error in progress polling:', error);
        onError('Failed to track progress. Please try again.');
      }
    };

    startGeneration();
  }, [workflowId, onComplete, onError]);

  const getCurrentStepIndex = () => {
    if (!currentStep) return 0;
    return generationSteps.findIndex(step => 
      currentStep.toLowerCase().includes(step.id.replace('_', ' '))
    );
  };

  const currentStepIndex = getCurrentStepIndex();

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="w-full max-w-4xl mx-auto space-y-6"
    >
      {/* Header */}
      <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
        <CardHeader className="text-center">
          <div className="flex justify-center mb-4">
            <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-600 rounded-full flex items-center justify-center">
              <Loader2 className="w-8 h-8 text-white animate-spin" />
            </div>
          </div>
          <CardTitle className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
            Generating Your Video
          </CardTitle>
          <CardDescription className="text-lg text-gray-600">
            We're creating your professional video with AI-generated images, voice narration, and background music.
          </CardDescription>
        </CardHeader>
      </Card>

      {/* Progress Bar */}
      <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
        <CardContent className="pt-6">
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-sm font-medium text-gray-700">Overall Progress</span>
              <span className="text-sm font-bold text-gray-900">
                {progress?.progress_percentage || 0}%
              </span>
            </div>
            <Progress value={progress?.progress_percentage || 0} className="h-3" />
            <p className="text-sm text-gray-600 text-center">
              {currentStep}
            </p>
            {progress?.estimated_time_remaining && (
              <p className="text-xs text-gray-500 text-center">
                Estimated time remaining: {progress.estimated_time_remaining} seconds
              </p>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Generation Steps */}
      <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
        <CardHeader>
          <CardTitle className="text-lg">Generation Steps</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {generationSteps.map((step, index) => {
              const isCompleted = index < currentStepIndex;
              const isActive = index === currentStepIndex;
              const isPending = index > currentStepIndex;

              return (
                <motion.div
                  key={step.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                  className={`flex items-center space-x-4 p-4 rounded-lg border transition-all duration-300 ${
                    isCompleted
                      ? 'bg-green-50 border-green-200'
                      : isActive
                      ? 'bg-blue-50 border-blue-200'
                      : 'bg-gray-50 border-gray-200'
                  }`}
                >
                  <div
                    className={`w-10 h-10 rounded-full flex items-center justify-center ${
                      isCompleted
                        ? 'bg-green-500 text-white'
                        : isActive
                        ? 'bg-blue-500 text-white'
                        : 'bg-gray-300 text-gray-600'
                    }`}
                  >
                    {isCompleted ? (
                      <div className="w-5 h-5 bg-white rounded-full flex items-center justify-center">
                        <div className="w-2 h-2 bg-green-500 rounded-full" />
                      </div>
                    ) : isActive ? (
                      <Loader2 className="w-5 h-5 animate-spin" />
                    ) : (
                      <step.icon className="w-5 h-5" />
                    )}
                  </div>
                  <div className="flex-1">
                    <h4
                      className={`font-medium ${
                        isCompleted
                          ? 'text-green-800'
                          : isActive
                          ? 'text-blue-800'
                          : 'text-gray-600'
                      }`}
                    >
                      {step.title}
                    </h4>
                    <p className="text-sm text-gray-500">
                      {isCompleted
                        ? 'Completed'
                        : isActive
                        ? 'In progress...'
                        : 'Pending'}
                    </p>
                  </div>
                </motion.div>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* Status Message */}
      <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
        <CardContent className="pt-6">
          <div className="text-center">
            <p className="text-sm text-gray-600">
              {isGenerating ? (
                <>
                  Generation is in progress... <br />
                  <span className="text-xs text-gray-500 mt-1">
                    Please don't close this page while generation is in progress
                  </span>
                </>
              ) : (
                'Processing...'
              )}
            </p>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
} 