import React from 'react';
import { cn } from '@/lib/utils';

interface ProgressProps extends React.HTMLAttributes<HTMLDivElement> {
  value: number;
  max?: number;
}

const Progress = React.forwardRef<HTMLDivElement, ProgressProps>(
  ({ className, value, max = 100, ...props }, ref) => {
    const percentage = Math.min((value / max) * 100, 100);
    
    return (
      <div
        ref={ref}
        className={cn('relative w-full overflow-hidden rounded-full bg-secondary', className)}
        {...props}
      >
        <div
          className="h-2 w-full flex-none transition-all duration-500 ease-out bg-primary"
          style={{ width: `${percentage}%` }}
        />
      </div>
    );
  }
);
Progress.displayName = 'Progress';

export { Progress }; 