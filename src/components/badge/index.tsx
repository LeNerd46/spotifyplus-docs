import React from 'react';
import styles from './styles.module.css';

interface BadgeProps {
    children: React.ReactNode;
    variant?: 'info' | 'success' | 'warning' | 'danger' | 'neutral';
    href?: string;
}

export default function Badge({ children, variant = 'info', href }: BadgeProps) {
    const className = `${styles.badge} ${styles[variant]}`;

    if (href) return <a href={href} className={className}>{children}</a>;

    return <span className={className}>{children}</span>;
}