import React, { useState } from 'react';

function PatternForm({ onFormSubmit, isLoading }) {
  const [itemType, setItemType] = useState('granny square');
  const [yarnSize, setYarnSize] = useState('worsted');
  const [hookSize, setHookSize] = useState('4.00mm');
  const [mode, setMode] = useState('strict');
  const [imageBlob, setImageBlob] = useState(null);
  const [previewUrl, setPreviewUrl] = useState('');

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setPreviewUrl(URL.createObjectURL(file));

    const reader = new FileReader();
    reader.onloadend = () => {
      setImageBlob(reader.result);
    };
    reader.readAsDataURL(file);
  };

  const submitAction = (e) => {
    e.preventDefault();
    if (!imageBlob) {
      alert('Please select or upload a target design image asset first.');
      return;
    }
    onFormSubmit({
      item_type: itemType,
      yarn_size: yarnSize,
      hook_size: hookSize,
      mode: mode,
      image: imageBlob
    });
  };

  return (
    <form onSubmit={submitAction} className="form-stack">
      <div className="form-group">
        <label>Target Object Classification Type</label>
        <select value={itemType} onChange={(e) => setItemType(e.target.value)}>
          <option value="granny square">Granny Square Block</option>
          <option value="beanie">Beanie Shell</option>
          <option value="scarf">Scarf Layout</option>
        </select>
      </div>

      <div className="form-group">
  <label>Yarn Weight / Size Allocation</label>

  <select
    value={yarnSize}
    onChange={(e) => setYarnSize(e.target.value)}
    required
  >
    <option value="lace">Lace</option>
    <option value="fingering">Fingering</option>
    <option value="sport">Sport</option>
    <option value="dk">DK</option>
    <option value="worsted">Worsted</option>
    <option value="aran">Aran</option>
    <option value="bulky">Bulky</option>
    <option value="super bulky">Super Bulky</option>
  </select>
</div>

      <div className="form-group">
        <label>Crochet Hook Sizing Specifications</label>
        <input 
          type="text" 
          value={hookSize} 
          onChange={(e) => setHookSize(e.target.value)} 
          placeholder="e.g., 3.5mm, 4mm, G-6"
          required 
        />
      </div>

      <div className="form-group">
        <label>AI Pattern Optimization Mode</label>
        <div className="radio-group">
          <label className="radio-label">
            <input type="radio" value="strict" checked={mode === 'strict'} onChange={() => setMode('strict')} />
            Strict Replication
          </label>
          <label className="radio-label">
            <input type="radio" value="creative" checked={mode === 'creative'} onChange={() => setMode('creative')} />
            Adaptive (Creative)
          </label>
        </div>
      </div>

      <div className="form-group">
        <label className="file-upload-zone">
          <span className="upload-btn">Choose Reference Image</span>
          <input type="file" accept="image/*" onChange={handleImageChange} style={{ display: 'none' }} />
        </label>
        {previewUrl && (
          <div className="thumbnail-wrapper">
            <img src={previewUrl} alt="Execution source snapshot preview" className="image-preview" />
          </div>
        )}
      </div>

      <button type="submit" disabled={isLoading} className="submit-action-btn">
        {isLoading ? 'Processing System Execution...' : 'Analyze & Build Pattern Matrix'}
      </button>
    </form>
  );
}

export default PatternForm;
