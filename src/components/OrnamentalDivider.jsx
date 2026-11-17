import React from 'react';

export default function OrnamentalDivider({ motif = '✦', className = '' }) {
  return (
    <div className={`ornamental-divider ${className}`} aria-hidden="true">
      <div className="ornamental-line" />
      <span className="ornamental-motif" style={{ color: 'var(--color-gold)' }}>
        {motif}
      </span>
      <div className="ornamental-line" />
    </div>
  );
}
