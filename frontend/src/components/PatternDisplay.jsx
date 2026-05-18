import React, { useState } from 'react';

function PatternDisplay({ outputData }) {
  const [showJsonInspector, setShowJsonInspector] = useState(false);
  const { image_quality, warning, pdf_url, raw_json } = outputData;

  // Determine label type context depending on geometry profile
  const isRowBased = raw_json?.detected_shape === 'rows' || raw_json?.detected_shape === 'row';
  const structuralStepLabel = isRowBased ? 'Row' : 'Round';

  // Helper function to safely unpack a stitch object or string
  const renderStitchItem = (item) => {
    if (!item) return null;
    
    if (typeof item === 'object') {
      const details = (
  item.instructions ||
  item.stitches ||
  item.instruction ||
  item.text ||
  JSON.stringify(item)
);
      const stepNum = item.round_number || item.round || '';
      const sideStitches = item.stitches_per_side;
      
      return (
        <span>
          {stepNum && <strong>{structuralStepLabel} {stepNum}: </strong>}
          {details}
          {sideStitches > 0 && <small className="stitch-count-tag"> ({sideStitches} sts per side)</small>}
          {item.total_stitches > 0 && <span className="total-count-badge"> Total: {item.total_stitches} sts</span>}
        </span>
      );
    }
    
    return <span>{String(item)}</span>;
  };

  // Helper function to safely unpack a color block object or string
  const renderColorItem = (item) => {
    if (!item) return null;

    if (typeof item === 'object') {
      const colorName = item.color || item.yarn_color || JSON.stringify(item);
      const stepNum = item.round || item.round_number || '';

      return (
        <span>
          {stepNum && <strong>{structuralStepLabel} {stepNum}: </strong>}
          {colorName}
        </span>
      );
    }

    return <span>{String(item)}</span>;
  };

  return (
    <div className="display-wrapper">
      {image_quality === 'low' && (
        <div className="quality-alert-banner">
          <p>⚠️ Low clear image quality detected. Generating approximation based on visible structure.</p>
          {warning && <small className="warning-subtext">{warning}</small>}
        </div>
      )}

      <div className="action-row">
        <a href={pdf_url} target="_blank" rel="noreferrer" className="action-download-btn">
          📥 Download Printable PDF Blueprint
        </a>
        <button 
          onClick={() => setShowJsonInspector(!showJsonInspector)} 
          className="secondary-btn"
        >
          {showJsonInspector ? 'Hide Raw AI Data Pipeline' : 'Inspect Clean Response Object JSON'}
        </button>
      </div>

      {showJsonInspector ? (
        <div className="json-container">
          <pre><code>{JSON.stringify(raw_json, null, 2)}</code></pre>
        </div>
      ) : (
        <div className="compiled-preview-area">
          <h3>Summary Overview</h3>
          <p className="summary-paragraph">{raw_json.summary}</p>
          
          <div className="metadata-badge-row">
            <span className="badge">Structure Layout: {raw_json.detected_shape}</span>
            <span className="badge">Difficulty: {raw_json.difficulty}</span>
            <span className="badge">Quality Rating: {image_quality}</span>
          </div>

          {raw_json.stitch_pattern?.starting_round && (
            <div className="starting-step-box">
              <strong>Setup Phase:</strong> {raw_json.stitch_pattern.starting_round}
            </div>
          )}

          <h4>Stitch Directives List Block</h4>
          <ol className="stitch-list">
            {raw_json.stitch_pattern?.rounds?.map((roundItem, idx) => (
              <li key={idx}>{renderStitchItem(roundItem)}</li>
            ))}
          </ol>

          {raw_json.color_changes && raw_json.color_changes.length > 0 && (
            <>
              <h4>Color Assignment Roadmap</h4>
              <ul className="bullet-list">
                {raw_json.color_changes.map((colorItem, idx) => (
                  <li key={idx}>{renderColorItem(colorItem)}</li>
                ))}
              </ul>
            </>
          )}

          {raw_json.notes && (
            <>
              <h4>Construction Notes</h4>
              <p className="notes-box">{raw_json.notes}</p>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default PatternDisplay;
