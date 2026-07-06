import React, { useState, useEffect, useRef } from "react";
import {
  Sparkles,
  Search,
  Building2,
  TrendingUp,
  FileText,
  Eye,
  Save,
  MessageSquare,
  Paperclip,
  Send,
  Sun,
  Moon,
  ChevronDown,
  CheckCheck,
  Shield,
  ArrowRight,
  X,
  FileSpreadsheet,
  AlertTriangle,
  Award
} from "lucide-react";
import { companyData } from "./companyData";
import "./App.css";

function App() {
  const [activeTab, setActiveTab] = useState("Chat Assistant");
  const [activeCompany, setActiveCompany] = useState("ASIANPAINT");
  const [theme, setTheme] = useState("light");
  const [inputVal, setInputVal] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  
  // Custom chat histories per company context
  const [chatHistory, setChatHistory] = useState([
    {
      id: 1,
      sender: "assistant",
      time: "10:41 AM",
      text: "Here is a detailed breakdown of the business segments and recent financial highlights for Asian Paints Limited (NSE: ASIANPAINT).",
      richContent: {
        sections: [
          {
            title: "Overview",
            content: "Asian Paints Limited is India's leading paint manufacturer and ranks among the top ten decorative coatings companies globally, operating in 15 countries with 26 manufacturing facilities."
          },
          {
            title: "Key Business Segments",
            bullets: [
              "**Decorative Paints (India)** – Largest revenue contributor, comprises interior/exterior wall paints, wood finishes, and SmartCare waterproofing systems.",
              "**Industrial Coatings** – Operated via PPG-Asian Paints JVs, servicing automotive OEM, refinishes, and heavy-duty protective coatings.",
              "**Home Décor & Ancillaries** – Integrated offerings including Sleek modular kitchens, Ess Ess bath fittings, and lighting/furniture through Beautiful Homes boutique network.",
              "**International Business** – Strategic operations in Middle East, South Asia, Africa, and South Pacific markets."
            ]
          },
          {
            title: "Recent Financial Highlights (FY24)",
            content: "Consolidated performance showing steady margins driven by lower input costs and strong volume performance in the domestic decorative division:"
          }
        ],
        table: [
          { segment: "Decorative India", value: "₹28,450 Cr", change: "+10.2% YoY", isPositive: true },
          { segment: "Home Décor & Service", value: "₹2,100 Cr", change: "+14.5% YoY", isPositive: true },
          { segment: "Industrial Coatings", value: "₹3,250 Cr", change: "+8.7% YoY", isPositive: true },
          { segment: "International Operations", value: "₹1,716 Cr", change: "-2.3% YoY", isPositive: false }
        ],
        closing: "Let me know if you would like more details on any specific segment, competitor comparison, or risk factor."
      }
    }
  ]);

  const chatEndRef = useRef(null);

  // Scroll to bottom of chat thread when history changes or typing state changes
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatHistory, isTyping]);

  // Set initial chat when changing active company context
  useEffect(() => {
    const comp = companyData[activeCompany];
    setChatHistory([
      {
        id: Date.now(),
        sender: "assistant",
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        text: `Switched analysis context to ${comp.fullName} (${comp.ticker}). Ask me anything about their operations, financials, or market standings.`,
        richContent: {
          sections: [
            {
              title: "Company Overview",
              content: `${comp.fullName} is currently trading at ${comp.price} (${comp.change}). Here is a summary of their core activities and operational segments.`
            },
            {
              title: "Business Segments",
              bullets: comp.highlights
            }
          ],
          table: comp.segments.map(s => ({
            segment: s.name,
            value: s.revenue,
            change: s.change,
            isPositive: s.isPositive
          })),
          closing: `Type a question below or click the quick chips to review recent performance, competitive advantages, or risks for ${comp.name}.`
        }
      }
    ]);
  }, [activeCompany]);

  const toggleTheme = () => {
    setTheme(prev => (prev === "light" ? "dark" : "light"));
  };

  const handleSelectCompany = (symbol) => {
    setActiveCompany(symbol);
    setIsModalOpen(false);
  };

  const parseMarkdown = (text) => {
    if (!text) return "";
    // Extremely basic parser for bold (**text**)
    const parts = text.split(/(\*\*.*?\*\*)/g);
    return parts.map((part, index) => {
      if (part.startsWith("**") && part.endsWith("**")) {
        return <strong key={index}>{part.slice(2, -2)}</strong>;
      }
      return part;
    });
  };

  // Generate fallback simulated response based on company and query
  const generateSimulatedResponse = (query, comp) => {
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const lowerQuery = query.toLowerCase();

    let title = "AI Assistant Analysis";
    let sections = [];
    let table = null;
    let closing = "Is there any other financial aspect of this company you'd like to dive into?";

    if (lowerQuery.includes("segment") || lowerQuery.includes("business") || lowerQuery.includes("operate")) {
      title = "Business Segment Analysis";
      sections = [
        {
          title: "Core Business Structure",
          content: `${comp.name} derives its revenue from multiple key segments. Each segment plays a unique role in the company's growth strategy.`
        },
        {
          title: "Segment Breakdown & Highlights",
          bullets: comp.highlights
        }
      ];
      table = comp.segments.map(s => ({
        segment: s.name,
        value: s.revenue,
        change: s.change,
        isPositive: s.isPositive
      }));
    } else if (lowerQuery.includes("perform") || lowerQuery.includes("recent") || lowerQuery.includes("financial") || lowerQuery.includes("revenue") || lowerQuery.includes("profit")) {
      title = "Financial Performance & Highlights";
      sections = [
        {
          title: "Financial Position overview",
          content: `${comp.fullName} is displaying robust metrics with a total Market Capitalization of ${comp.marketCap}. The stock currently trades at a P/E Ratio of ${comp.peRatio} and yields an ROE of ${comp.roe}.`
        },
        {
          title: "Key Performance Drivers",
          bullets: [
            ...comp.highlights.slice(0, 2),
            `**Leverage Profile** – Debt to equity stands at a comfortable ${comp.debtToEquity}, indicating strong capital adequacy.`,
            `**Investor Return** – Consistent return on equity (${comp.roe}) driven by operational cost optimization and strategic price adjustments.`
          ]
        }
      ];
      table = comp.segments.map(s => ({
        segment: s.name,
        value: s.revenue,
        change: s.change,
        isPositive: s.isPositive
      }));
    } else if (lowerQuery.includes("advantage") || lowerQuery.includes("competit") || lowerQuery.includes("strength") || lowerQuery.includes("moat")) {
      title = "Competitive Advantages (Moat)";
      sections = [
        {
          title: "Market Strengths",
          bullets: comp.advantages
        },
        {
          title: "Strategic Overview",
          content: `${comp.name} leverages its brand equity and infrastructure to maintain high entry barriers for new competitors, resulting in consistent pricing power and industry-leading margins.`
        }
      ];
    } else if (lowerQuery.includes("risk") || lowerQuery.includes("threat") || lowerQuery.includes("weakness") || lowerQuery.includes("challenge")) {
      title = "Risk Factors & Key Challenges";
      sections = [
        {
          title: "Identified Risks",
          bullets: comp.risks
        },
        {
          title: "Risk Mitigation Strategy",
          content: `The management remains cautious and is proactively taking measures to diversify supply chains, hedge raw material imports, and introduce mid-tier and budget offerings to defend its market share.`
        }
      ];
    } else {
      // General question
      title = "General Context Inquiry";
      sections = [
        {
          title: `Context Summary: ${comp.name}`,
          content: `Based on public filings and recent company reports, ${comp.fullName} is positioned strongly with a stock price of ${comp.price} (${comp.change}).`
        },
        {
          title: "Key Insights",
          bullets: comp.highlights
        }
      ];
      table = comp.segments.map(s => ({
        segment: s.name,
        value: s.revenue,
        change: s.change,
        isPositive: s.isPositive
      }));
    }

    return {
      id: Date.now(),
      sender: "assistant",
      time,
      text: `Based on context from ${comp.name}'s latest filings, here is the structured analysis regarding "${query}":`,
      richContent: {
        sections,
        table,
        closing
      }
    };
  };

  const handleSend = async (text) => {
    if (!text.trim()) return;

    const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const userMsg = {
      id: Date.now(),
      sender: "user",
      time: currentTime,
      text: text
    };

    setChatHistory(prev => [...prev, userMsg]);
    setInputVal("");
    setIsTyping(true);

    // Call actual backend first. If it fails, fallback to simulated client-side logic.
    try {
      const response = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          question: text,
          symbol: activeCompany
        })
      });

      if (!response.ok) {
        throw new Error("Backend response not OK");
      }

      // Handle streaming response from FastAPI backend
      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let done = false;
      let streamedText = "";

      // Add a placeholder assistant response that we will update as stream chunks arrive
      const assistantMsgId = Date.now() + 1;
      setChatHistory(prev => [...prev, {
        id: assistantMsgId,
        sender: "assistant",
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        text: ""
      }]);
      setIsTyping(false);

      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;
        if (value) {
          const chunk = decoder.decode(value, { stream: !done });
          streamedText += chunk;
          
          setChatHistory(prev => prev.map(msg => {
            if (msg.id === assistantMsgId) {
              // Parse basic headers or tables in the streamed response
              return {
                ...msg,
                text: streamedText
              };
            }
            return msg;
          }));
        }
      }
    } catch (error) {
      console.warn("Backend `/ask` unavailable. Falling back to local data matching spec.", error);
      
      // Simulate typing delay for realism
      setTimeout(() => {
        const comp = companyData[activeCompany];
        const simulatedReply = generateSimulatedResponse(text, comp);
        setChatHistory(prev => [...prev, simulatedReply]);
        setIsTyping(false);
      }, 1000);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleSend(inputVal);
    }
  };

  const comp = companyData[activeCompany];

  // Filter companies based on search in modal
  const filteredCompanies = Object.keys(companyData).filter(sym => 
    sym.toLowerCase().includes(searchQuery.toLowerCase()) || 
    companyData[sym].name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div id="root" className={theme === "dark" ? "dark-mode" : ""}>
      <div className="app-shell">
        {/* 1. SIDEBAR */}
        <aside className="sidebar">
          <div className="sidebar-top">
            <div className="logo-block">
              <div className="logo-row">
                <div className="logo-icon-bg">
                  <TrendingUp size={20} strokeWidth={2.5} />
                </div>
                <span className="logo-wordmark">
                  MONEY <span>LOGIX</span>
                </span>
              </div>
              <span className="logo-subtitle">AI Financial Assistant</span>
            </div>

            <nav>
              <ul className="nav-list">
                <li 
                  className={`nav-item ${activeTab === "Chat Assistant" ? "active" : ""}`}
                  onClick={() => setActiveTab("Chat Assistant")}
                >
                  <MessageSquare size={18} />
                  Chat Assistant
                </li>
                <li 
                  className={`nav-item ${activeTab === "Companies" ? "active" : ""}`}
                  onClick={() => {
                    setActiveTab("Companies");
                    setIsModalOpen(true);
                  }}
                >
                  <Building2 size={18} />
                  Companies
                </li>
                <li 
                  className={`nav-item ${activeTab === "Financial Reports" ? "active" : ""}`}
                  onClick={() => setActiveTab("Financial Reports")}
                >
                  <FileText size={18} />
                  Financial Reports
                </li>
                <li 
                  className={`nav-item ${activeTab === "Market Insights" ? "active" : ""}`}
                  onClick={() => setActiveTab("Market Insights")}
                >
                  <TrendingUp size={18} />
                  Market Insights
                </li>
                <li 
                  className={`nav-item ${activeTab === "Watchlist" ? "active" : ""}`}
                  onClick={() => setActiveTab("Watchlist")}
                >
                  <Eye size={18} />
                  Watchlist
                </li>
                <li 
                  className={`nav-item ${activeTab === "Saved Chats" ? "active" : ""}`}
                  onClick={() => setActiveTab("Saved Chats")}
                >
                  <Save size={18} />
                  Saved Chats
                </li>
              </ul>
            </nav>
          </div>

          <div className="sidebar-bottom">
            <div className="promo-card">
              <div className="promo-header">
                <Sparkles size={16} />
                <span>Powered by AI</span>
              </div>
              <p className="promo-desc">
                Analyzing raw public filings and market charts to synthesize structured insights.
              </p>
              <div className="promo-wave"></div>
            </div>
            <div className="sidebar-footer">
              <p>© 2025 Money Logix</p>
              <p>All rights reserved.</p>
            </div>
          </div>
        </aside>

        {/* 2. MAIN PANEL */}
        <main className="main-panel">
          {/* Header */}
          <header className="main-header">
            <div className="header-left">
              <h1>Good morning, Analyst 👋</h1>
              <p>Ask anything about companies, financials, markets and more.</p>
            </div>
            <div className="header-right">
              <button className="theme-toggle-btn" onClick={toggleTheme} title="Toggle Theme">
                {theme === "light" ? <Moon size={18} /> : <Sun size={18} />}
              </button>
              
              <div className="user-profile" onClick={() => setIsModalOpen(true)}>
                <div className="user-avatar">A</div>
                <span className="user-name">Analyst</span>
                <ChevronDown size={14} className="user-chevron" />
              </div>
            </div>
          </header>

          {/* Chat Workspace (If Chat Assistant is selected) */}
          {activeTab === "Chat Assistant" ? (
            <>
              <div className="chat-container">
                <div className="chat-card">
                  <div className="chat-card-header">
                    <div className="chat-card-title-row">
                      <Sparkles size={18} />
                      <h2>AI Financial Assistant</h2>
                    </div>
                    <div className="status-pill">
                      <span className="status-dot pulse"></span>
                      <span>Online</span>
                    </div>
                  </div>

                  {/* Scrollable Chat Thread */}
                  <div className="chat-thread-scroller">
                    {chatHistory.map((msg) => (
                      <div key={msg.id} className={msg.sender === "user" ? "user-msg-row animate-fade-in" : "assistant-msg-row animate-fade-in"}>
                        {msg.sender === "assistant" && (
                          <div className="assistant-avatar">
                            <TrendingUp size={16} />
                          </div>
                        )}
                        
                        {msg.sender === "user" ? (
                          <div className="user-bubble">
                            <p>{msg.text}</p>
                            <div className="user-msg-meta">
                              <span>{msg.time}</span>
                              <CheckCheck size={14} />
                            </div>
                          </div>
                        ) : (
                          <div className="assistant-content-block">
                            <p>{msg.text}</p>
                            
                            {msg.richContent && (
                              <>
                                {msg.richContent.sections?.map((sec, idx) => (
                                  <div key={idx}>
                                    <h3 className="section-header">{sec.title}</h3>
                                    {sec.content && <p>{sec.content}</p>}
                                    {sec.bullets && (
                                      <ul>
                                        {sec.bullets.map((bullet, bIdx) => (
                                          <li key={bIdx}>{parseMarkdown(bullet)}</li>
                                        ))}
                                      </ul>
                                    )}
                                  </div>
                                ))}
                                
                                {msg.richContent.table && (
                                  <div className="data-table-container animate-fade-in">
                                    <table className="data-table">
                                      <tbody>
                                        {msg.richContent.table.map((row, rIdx) => (
                                          <tr key={rIdx}>
                                            <td className="table-label-cell">
                                              <Building2 size={14} />
                                              {row.segment}
                                            </td>
                                            <td className="table-value-cell">{row.value}</td>
                                            <td className="table-change-cell">
                                              <span className={row.isPositive ? "change-pill-positive" : "change-pill-negative"}>
                                                {row.change}
                                              </span>
                                            </td>
                                          </tr>
                                        ))}
                                      </tbody>
                                    </table>
                                  </div>
                                )}
                                
                                {msg.richContent.closing && (
                                  <p style={{ marginTop: "8px", fontStyle: "italic", fontSize: "13.5px" }}>
                                    {msg.richContent.closing}
                                  </p>
                                )}
                              </>
                            )}
                            <div className="assistant-msg-meta">
                              <span>{msg.time}</span>
                            </div>
                          </div>
                        )}
                      </div>
                    ))}

                    {/* Typing Indicator */}
                    {isTyping && (
                      <div className="assistant-msg-row animate-fade-in">
                        <div className="assistant-avatar">
                          <TrendingUp size={16} />
                        </div>
                        <div className="typing-indicator">
                          <span className="typing-dot"></span>
                          <span className="typing-dot"></span>
                          <span className="typing-dot"></span>
                        </div>
                      </div>
                    )}
                    <div ref={chatEndRef} />
                  </div>

                  {/* Quick Actions Row */}
                  <div className="quick-action-row">
                    <button className="chip-btn" onClick={() => handleSend("What are the key business segments?")}>
                      <Building2 size={14} />
                      <span>Business segments</span>
                    </button>
                    <button className="chip-btn" onClick={() => handleSend("Analyze recent performance and metrics")}>
                      <TrendingUp size={14} />
                      <span>Recent performance</span>
                    </button>
                    <button className="chip-btn" onClick={() => handleSend("What are their competitive advantages?")}>
                      <Award size={14} style={{ color: "#3B82F6" }} />
                      <span>Competitive advantages</span>
                    </button>
                    <button className="chip-btn" onClick={() => handleSend("What are the primary risk factors?")}>
                      <AlertTriangle size={14} style={{ color: "var(--warning-amber)" }} />
                      <span>Risks</span>
                    </button>
                  </div>
                </div>
              </div>

              {/* Chat Input Bar */}
              <div className="input-area-container">
                <div className="input-bar-row">
                  <button className="input-icon-btn" title="Attach Document" onClick={() => alert("File attachment coming soon!")}>
                    <Paperclip size={18} />
                  </button>
                  <input
                    type="text"
                    className="chat-input"
                    placeholder={`Ask a question about ${comp.name}, financials, or market trends...`}
                    value={inputVal}
                    onChange={(e) => setInputVal(e.target.value)}
                    onKeyDown={handleKeyPress}
                  />
                  <button className="send-btn" onClick={() => handleSend(inputVal)} title="Send Message">
                    <Send size={16} />
                  </button>
                </div>
                <span className="input-disclaimer">
                  Money Logix can make mistakes. Please verify important information.
                </span>
              </div>
            </>
          ) : (
            // Fallback content when other navigation items are selected
            <div className="chat-container" style={{ justifyContent: "center", alignItems: "center", height: "100%", gap: "16px" }}>
              <div className="logo-icon-bg" style={{ width: "64px", height: "64px", borderRadius: "16px" }}>
                <Building2 size={32} />
              </div>
              <h2 style={{ fontSize: "20px", fontWeight: "700" }}>{activeTab} Dashboard</h2>
              <p style={{ color: "var(--text-secondary)", fontSize: "14px", maxWidth: "400px", textAlign: "center" }}>
                This section integrates companies, markets data, and folders. You are currently viewing the context of <strong>{comp.fullName}</strong>.
              </p>
              <button className="chip-btn" style={{ padding: "10px 20px" }} onClick={() => setActiveTab("Chat Assistant")}>
                Return to Chat Assistant
              </button>
            </div>
          )}
        </main>

        {/* 3. RIGHT PANEL */}
        <aside className="right-panel">
          {/* Card 1: Selected Company */}
          <div className="info-card">
            <div className="info-card-header">
              <Building2 size={16} />
              <h3>Selected Company</h3>
            </div>
            
            <div className="company-summary">
              <div className="company-logo-avatar">
                {comp.symbol.slice(0, 2)}
              </div>
              <div className="company-info-text">
                <div className="company-name">{comp.name}</div>
                <div className="company-fullname">{comp.fullName}</div>
              </div>
            </div>

            <div className="ticker-pill">{comp.ticker}</div>

            <div className="price-row">
              <span className="price-value">{comp.price}</span>
              <span className={comp.isPositive ? "change-pill-positive" : "change-pill-negative"}>
                {comp.change}
              </span>
            </div>
            <span className="price-timestamp">As of 24 May 2025, 10:40 AM IST</span>
            
            <button className="footer-link" onClick={() => setIsModalOpen(true)}>
              Change Company Context <ArrowRight size={14} />
            </button>
          </div>

          {/* Card 2: Key Metrics */}
          <div className="info-card">
            <div className="info-card-header">
              <TrendingUp size={16} />
              <h3>Key Metrics (FY24)</h3>
            </div>

            <div className="metrics-list">
              <div className="metric-row">
                <span className="metric-label">Market Cap</span>
                <span className="metric-val">{comp.marketCap}</span>
              </div>
              <div className="metric-row">
                <span className="metric-label">P/E Ratio</span>
                <span className="metric-val">{comp.peRatio}</span>
              </div>
              <div className="metric-row">
                <span className="metric-label">ROE</span>
                <span className="metric-val">{comp.roe}</span>
              </div>
              <div className="metric-row">
                <span className="metric-label">Debt to Equity</span>
                <span className="metric-val">{comp.debtToEquity}</span>
              </div>
            </div>

            <button className="footer-link" onClick={() => setActiveTab("Financial Reports")}>
              View Detailed Financials <ArrowRight size={14} />
            </button>
          </div>

          {/* Card 3: Relevant Reports */}
          <div className="info-card">
            <div className="info-card-header">
              <FileText size={16} />
              <h3>Relevant Reports</h3>
            </div>

            <div className="reports-list">
              {comp.reports.map((report, idx) => (
                <div key={idx} className="report-item" onClick={() => alert(`Downloading ${report.name}...`)}>
                  <div className="pdf-icon-wrapper">
                    <FileSpreadsheet size={16} />
                  </div>
                  <div className="report-meta-info">
                    <span className="report-title">{report.name}</span>
                    <span className="report-meta-text">PDF • {report.size}</span>
                  </div>
                </div>
              ))}
            </div>

            <button className="footer-link" onClick={() => setActiveTab("Financial Reports")}>
              View All Reports <ArrowRight size={14} />
            </button>
          </div>

          {/* Card 4: Bottom Banner */}
          <div className="disclaimer-card">
            <Shield size={18} />
            <p className="disclaimer-text">
              All data is sourced from reliable financial reports and public filings.
            </p>
          </div>
        </aside>
      </div>

      {/* Company Selector Modal */}
      {isModalOpen && (
        <div className="modal-backdrop" onClick={() => setIsModalOpen(false)}>
          <div className="modal-content animate-fade-in" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close-btn" onClick={() => setIsModalOpen(false)}>
              <X size={20} />
            </button>
            <h2 className="modal-title">Select Company Context</h2>
            
            <div className="input-bar-row" style={{ margin: "8px 0" }}>
              <Search size={16} className="user-chevron" />
              <input
                type="text"
                placeholder="Search from 20 available companies..."
                className="chat-input"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              {searchQuery && (
                <button className="input-icon-btn" onClick={() => setSearchQuery("")} style={{ width: "24px", height: "24px" }}>
                  <X size={14} />
                </button>
              )}
            </div>

            <div className="company-grid">
              {filteredCompanies.map((symbol) => {
                const c = companyData[symbol];
                return (
                  <div
                    key={symbol}
                    className={`company-select-card ${activeCompany === symbol ? "active" : ""}`}
                    onClick={() => handleSelectCompany(symbol)}
                  >
                    <div className="company-select-symbol">{symbol}</div>
                    <div className="company-select-name">{c.name}</div>
                  </div>
                );
              })}
              {filteredCompanies.length === 0 && (
                <div style={{ gridColumn: "1 / -1", padding: "20px", color: "var(--text-secondary)", fontSize: "13px" }}>
                  No companies found matching "{searchQuery}"
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
