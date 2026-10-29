// Adapted from shadcn/ui (MIT), https://github.com/shadcn-ui/ui
import React from 'react';
import { Slot } from '@radix-ui/react-slot';
import { cva } from 'class-variance-authority';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';
const variants = cva('button', {variants:{variant:{default:'button-primary',outline:'button-outline',ghost:'button-ghost'}},defaultVariants:{variant:'default'}});
export function Button({className,variant,asChild=false,...props}) { const Component=asChild?Slot:'button'; return <Component className={twMerge(clsx(variants({variant}),className))} {...props}/>; }
