import { useState, useEffect, useRef } from "react";
import { Play, Copy, Check, ChevronDown, ChevronRight, Image as ImageIcon } from "lucide-react";

// Render markdown-like text (basic)
function renderMarkdownText(text) {
  if (!text) return "";
  let html = text
    .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre class="nb-code-block"><code>$2</code></pre>')
    .replace(/`([^`]+)`/g, '<code class="nb-inline-code">$1</code>')
    .replace(/\*\*\*(.+?)\*\*\*/g, "<strong><em>$1</em></strong>")
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.+?)\*/g, "<em>$1</em>")
    .replace(/^### (.+)$/gm, '<h3 class="nb-h3">$1</h3>')
    .replace(/^## (.+)$/gm, '<h2 class="nb-h2">$1</h2>')
    .replace(/^# (.+)$/gm, '<h1 class="nb-h1">$1</h1>')
    .replace(/^- (.+)$/gm, '<li class="nb-li">$1</li>')
    .replace(/^(\d+)\. (.+)$/gm, '<li class="nb-li-num">$2</li>')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" class="nb-link">$1</a>')
    .replace(/^---$/gm, '<hr class="nb-hr"/>')
    .replace(/\n\n/g, '<br/><br/>');
  return html;
}

function MarkdownCell({ source }) {
  const text = Array.isArray(source) ? source.join("") : source;
  return (
    <div
      className="nb-markdown-cell"
      dangerouslySetInnerHTML={{ __html: renderMarkdownText(text) }}
    />
  );
}

function CodeCell({ source, outputs, executionCount }) {
  const [copied, setCopied] = useState(false);
  const [collapsed, setCollapsed] = useState(false);
  const code = Array.isArray(source) ? source.join("") : source;

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="nb-code-cell">
      <div className="nb-code-header">
        <div className="nb-code-label">
          <button onClick={() => setCollapsed(!collapsed)} className="nb-collapse-btn">
            {collapsed ? <ChevronRight size={14} /> : <ChevronDown size={14} />}
          </button>
          <Play size={12} className="nb-play-icon" />
          <span>In [{executionCount || " "}]</span>
        </div>
        <button onClick={handleCopy} className="nb-copy-btn">
          {copied ? <Check size={14} /> : <Copy size={14} />}
        </button>
      </div>
      {!collapsed && (
        <>
          <pre className="nb-code-content">
            <code>{code}</code>
          </pre>
          {outputs && outputs.length > 0 && (
            <div className="nb-output">
              <div className="nb-output-label">
                <span>Out [{executionCount || " "}]</span>
              </div>
              <div className="nb-output-content">
                {outputs.map((output, i) => (
                  <OutputRenderer key={i} output={output} />
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}

function OutputRenderer({ output }) {
  if (output.output_type === "stream") {
    const text = Array.isArray(output.text) ? output.text.join("") : output.text;
    return <pre className="nb-stream">{text}</pre>;
  }

  if (output.output_type === "execute_result" || output.output_type === "display_data") {
    const data = output.data;
    if (data) {
      if (data["image/png"]) {
        return <img src={`data:image/png;base64,${data["image/png"]}`} alt="output" className="nb-image" />;
      }
      if (data["text/html"]) {
        const html = Array.isArray(data["text/html"]) ? data["text/html"].join("") : data["text/html"];
        return <div className="nb-html-output" dangerouslySetInnerHTML={{ __html: html }} />;
      }
      if (data["text/plain"]) {
        const text = Array.isArray(data["text/plain"]) ? data["text/plain"].join("") : data["text/plain"];
        return <pre className="nb-plain">{text}</pre>;
      }
    }
  }

  if (output.output_type === "error") {
    const traceback = output.traceback
      ? output.traceback.join("\n").replace(/\x1b\[[0-9;]*m/g, "")
      : `${output.ename}: ${output.evalue}`;
    return <pre className="nb-error">{traceback}</pre>;
  }

  return null;
}

// Render a Markdown file
function MarkdownFileRenderer({ content }) {
  return (
    <div className="nb-markdown-cell" dangerouslySetInnerHTML={{ __html: renderMarkdownText(content) }} />
  );
}

export default function NotebookRenderer({ filepath, isMd }) {
  const [notebook, setNotebook] = useState(null);
  const [mdContent, setMdContent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const containerRef = useRef(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    setNotebook(null);
    setMdContent(null);

    fetch(encodeURI(filepath))
      .then((res) => {
        if (!res.ok) throw new Error(`Fichier non trouvé: ${filepath}`);
        return isMd ? res.text() : res.json();
      })
      .then((data) => {
        if (isMd) {
          setMdContent(data);
        } else {
          setNotebook(data);
        }
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, [filepath, isMd]);

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = 0;
    }
  }, [notebook, mdContent]);

  if (loading) {
    return (
      <div className="nb-loading">
        <div className="nb-spinner"></div>
        <p>Chargement du cours...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="nb-error-state">
        <div className="nb-error-icon">📄</div>
        <h3>Fichier non disponible</h3>
        <p>{error}</p>
        <p className="nb-error-hint">
          Assurez-vous que le fichier notebook est bien placé dans le dossier <code>public/courses/</code>
        </p>
      </div>
    );
  }

  if (isMd && mdContent) {
    return (
      <div className="nb-container" ref={containerRef}>
        <MarkdownFileRenderer content={mdContent} />
      </div>
    );
  }

  if (!notebook || !notebook.cells) {
    return (
      <div className="nb-error-state">
        <h3>Format de notebook invalide</h3>
      </div>
    );
  }

  return (
    <div className="nb-container" ref={containerRef}>
      {notebook.cells.map((cell, index) => {
        if (cell.cell_type === "markdown") {
          return <MarkdownCell key={index} source={cell.source} />;
        }
        if (cell.cell_type === "code") {
          return (
            <CodeCell
              key={index}
              source={cell.source}
              outputs={cell.outputs}
              executionCount={cell.execution_count}
            />
          );
        }
        return null;
      })}
    </div>
  );
}
