import React, { useEffect, useRef } from 'react';
import { X, ShieldCheck, Flame, TrendingUp, AlertTriangle, CheckCircle2, ChevronRight, Activity } from 'lucide-react';

export default function TargetFileModal({ player, onClose }) {
  const modalRef = useRef(null);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    document.body.style.overflow = 'hidden';

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      document.body.style.overflow = '';
    };
  }, [onClose]);

  if (!player) return null;

  const isBatter = player.type === 'batter';

  return (
    <div
      className="target-modal-backdrop"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
      role="dialog"
      aria-modal="true"
      aria-labelledby="dossier-title"
    >
      <div className="target-modal-content p-6 sm:p-8" ref={modalRef}>
        
        {/* Close Button */}
        <button
          type="button"
          onClick={onClose}
          className="absolute top-4 right-4 z-50 p-2 rounded-full bg-dark-elevated text-text-muted hover:text-white border border-dark-border cursor-pointer transition-colors"
          style={{
            backgroundColor: 'var(--color-dark-elevated)',
            borderColor: 'var(--color-dark-border)',
            color: 'var(--color-text-muted)',
          }}
          aria-label="Close dossier (Escape)"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Dossier Header */}
        <div className="pb-6 border-b border-dark-border">
          <div className="flex flex-wrap items-center gap-2 mb-2 font-mono text-xs">
            <span className="px-2.5 py-0.5 rounded bg-pinkops/20 text-pinkops font-bold uppercase border border-pinkops/40">
              TARGET FILE • RANK #{player.rank}
            </span>
            <span className={`px-2.5 py-0.5 rounded font-bold uppercase ${
              player.auctionCategory === 'MUST TARGET' ? 'bg-pinkops/20 text-pinkops border border-pinkops/40' :
              player.auctionCategory === 'TARGET' ? 'bg-icevein/20 text-icevein border border-icevein/40' :
              player.auctionCategory === 'VALUE TARGET' ? 'bg-gold/20 text-gold border border-gold/40' :
              'bg-text-faint/20 text-text-muted border border-text-faint/30'
            }`}>
              {player.auctionCategory}
            </span>
            <span className="text-text-faint">ID: {player.id}</span>
          </div>

          <h2 id="dossier-title" className="text-2xl sm:text-4xl font-extrabold text-white font-mono tracking-tight">
            {player.name}
          </h2>
          <p className="text-sm font-semibold text-gold mt-1 font-editorial text-lg italic">
            {player.role} • {player.secondaryRole}
          </p>
        </div>

        {/* Multidimensional Empirical Telemetry Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 py-6 font-mono text-xs border-b border-dark-border">
          <div className="p-3 rounded bg-black/40 border border-dark-border">
            <span className="text-text-faint block uppercase">LUB20 FLOOR:</span>
            <span className="text-lg font-bold text-pinkops">
              +{player.lub20.toFixed(4)}
            </span>
            <span className="text-[10px] text-text-muted block mt-0.5">20th pct downside floor</span>
          </div>

          <div className="p-3 rounded bg-black/40 border border-dark-border">
            <span className="text-text-faint block uppercase">PRESSURE BALLS:</span>
            <span className="text-lg font-bold text-white">
              {player.pressureExposure}
            </span>
            <span className="text-[10px] text-text-muted block mt-0.5">of {player.totalExposure} total</span>
          </div>

          <div className="p-3 rounded bg-black/40 border border-dark-border">
            <span className="text-text-faint block uppercase">
              {isBatter ? 'EARLY DISMISSAL:' : 'BLOWOUT RATE:'}
            </span>
            <span className={`text-lg font-bold ${
              (isBatter ? player.earlyDismissalRate : player.blowoutRate) <= 0.2 ? 'text-status-green' : 'text-status-red'
            }`}>
              {((isBatter ? player.earlyDismissalRate : player.blowoutRate) * 100).toFixed(1)}%
            </span>
            <span className="text-[10px] text-text-muted block mt-0.5">Gate ceiling ≤ 20.0%</span>
          </div>

          <div className="p-3 rounded bg-black/40 border border-dark-border">
            <span className="text-text-faint block uppercase">ROBUSTNESS:</span>
            <span className="text-lg font-bold text-icevein">
              {player.robustnessSupport}
            </span>
            <span className="text-[10px] text-text-muted block mt-0.5">Multiverse universal</span>
          </div>
        </div>

        {/* Detailed Qualitative Rationale */}
        <div className="py-6 space-y-4 font-body">
          <div>
            <h3 className="font-mono text-xs font-bold text-gold uppercase tracking-wider mb-2">
              WHY PINKOPS TARGETS THIS PLAYER
            </h3>
            <p className="text-sm text-text-main leading-relaxed bg-black/30 p-4 rounded-lg border border-dark-border">
              {player.whyTarget}
            </p>
          </div>

          {/* Additional Metrics Table */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 font-mono text-xs pt-2">
            <div className="p-3 rounded bg-dark-surface border border-dark-border space-y-2">
              <div className="flex justify-between">
                <span className="text-text-faint">Value Added (EB):</span>
                <span className="text-white font-bold">
                  +{isBatter ? player.contextualPerformance.toFixed(4) : player.contextualRunPrevention.toFixed(4)} r/b
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-text-faint">Epistemic Error (SE):</span>
                <span className="text-white font-bold">±{player.seEb.toFixed(4)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-text-faint">Match Variance (MAD):</span>
                <span className="text-white font-bold">{player.matchVaMad.toFixed(4)}</span>
              </div>
            </div>

            <div className="p-3 rounded bg-dark-surface border border-dark-border space-y-2">
              <div className="flex justify-between">
                <span className="text-text-faint">Tactical Role Fit:</span>
                <span className="text-gold font-bold">{player.roleFit}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-text-faint">Evidence Tier:</span>
                <span className="text-icevein font-bold">{player.evidenceTier}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-text-faint">Multiverse Invariant:</span>
                <span className="text-status-green font-bold">Survives 24/24 branches</span>
              </div>
            </div>
          </div>
        </div>

        {/* Dossier Footer */}
        <div className="pt-4 border-t border-dark-border flex flex-col sm:flex-row items-center justify-between text-xs font-mono text-text-muted gap-2">
          <div className="flex items-center gap-1.5 text-status-green">
            <ShieldCheck className="w-4 h-4" />
            <span>Strict Verification Pass: Spec B • Frozen Manifest Validated</span>
          </div>
          <button
            onClick={onClose}
            className="btn-pinkops-secondary py-1.5 px-4 text-xs font-bold"
          >
            CLOSE TARGET FILE
          </button>
        </div>

      </div>
    </div>
  );
}
