"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { MessageCircle, X, Send, Loader2, Sparkles } from "lucide-react"
import { chatAction, type ChatMessage } from "@/lib/api-actions"

export function AIChat() {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus()
    }
  }, [isOpen])

  const handleSend = async () => {
    const trimmed = input.trim()
    if (!trimmed || isLoading) return

    const userMessage: ChatMessage = { role: "user", content: trimmed }
    const updatedMessages = [...messages, userMessage]
    setMessages(updatedMessages)
    setInput("")
    setIsLoading(true)

    const result = await chatAction(trimmed, messages)

    if (result.data) {
      setMessages([...updatedMessages, { role: "assistant", content: result.data.reply }])
    } else {
      setMessages([...updatedMessages, { role: "assistant", content: `Sorry, I couldn't process that: ${result.error}` }])
    }

    setIsLoading(false)
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const suggestedQuestions = [
    "What climate clauses worked in African restructurings?",
    "Compare Zambia and Ghana's debt treatments",
    "What NPV reductions are realistic for LMICs?",
  ]

  return (
    <>
      {/* Floating button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 z-50 gradient-navy text-white rounded-full p-4 shadow-xl shadow-[#1e3a5f]/30 hover:opacity-90 transition-all hover:scale-105 group"
          aria-label="Open AI Advisor chat"
        >
          <MessageCircle className="h-6 w-6" />
          <span className="absolute -top-1 -right-1 w-3 h-3 bg-[#f59e0b] rounded-full animate-pulse" />
        </button>
      )}

      {/* Chat panel */}
      {isOpen && (
        <div className="fixed bottom-6 right-6 z-50 w-[400px] max-w-[calc(100vw-2rem)] h-[560px] max-h-[calc(100vh-3rem)] flex flex-col rounded-2xl shadow-2xl shadow-[#1e3a5f]/20 border border-[#1e3a5f]/15 bg-white overflow-hidden">
          {/* Header */}
          <div className="gradient-navy px-5 py-4 flex items-center justify-between flex-shrink-0">
            <div className="flex items-center gap-3">
              <div className="p-1.5 bg-white/15 rounded-lg">
                <Sparkles className="h-5 w-5 text-white" />
              </div>
              <div>
                <h3 className="text-white font-semibold text-sm">AI Advisor</h3>
                <p className="text-white/50 text-xs">Debt restructuring intelligence</p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="text-white/60 hover:text-white transition-colors p-1"
              aria-label="Close chat"
            >
              <X className="h-5 w-5" />
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto px-4 py-4 space-y-4 bg-slate-50/50">
            {messages.length === 0 && (
              <div className="space-y-4 pt-2">
                <div className="text-center">
                  <div className="inline-flex p-3 rounded-full bg-[#1e3a5f]/10 mb-3">
                    <Sparkles className="h-6 w-6 text-[#1e3a5f]" />
                  </div>
                  <p className="text-sm text-slate-600 font-medium">Ask me about debt restructuring</p>
                  <p className="text-xs text-slate-400 mt-1">
                    I have access to {20} verified precedents across {23} countries
                  </p>
                </div>
                <div className="space-y-2">
                  {suggestedQuestions.map((q, i) => (
                    <button
                      key={i}
                      onClick={() => { setInput(q); inputRef.current?.focus() }}
                      className="w-full text-left text-xs px-3 py-2.5 rounded-lg border border-[#1e3a5f]/10 bg-white text-slate-600 hover:bg-[#1e3a5f]/5 hover:border-[#1e3a5f]/20 transition-colors"
                    >
                      {q}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {messages.map((msg, i) => (
              <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                <div
                  className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                    msg.role === "user"
                      ? "gradient-navy text-white rounded-br-md"
                      : "bg-white border border-slate-200 text-slate-700 rounded-bl-md shadow-sm"
                  }`}
                >
                  {msg.role === "assistant" ? (
                    <div
                      className="[&_strong]:text-[#1e3a5f] [&_strong]:font-semibold [&_p]:mb-2 [&_p:last-child]:mb-0 [&_ul]:my-2 [&_ul]:pl-4 [&_ul]:list-disc [&_ul]:space-y-1 [&_ol]:my-2 [&_ol]:pl-4 [&_ol]:list-decimal [&_ol]:space-y-1 [&_li]:text-sm"
                      dangerouslySetInnerHTML={{ __html: formatChatMessage(msg.content) }}
                    />
                  ) : (
                    msg.content
                  )}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-white border border-slate-200 rounded-2xl rounded-bl-md px-4 py-3 shadow-sm">
                  <div className="flex items-center gap-2 text-sm text-slate-500">
                    <Loader2 className="h-4 w-4 animate-spin" />
                    <span>Analyzing...</span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="border-t border-slate-200 px-4 py-3 bg-white flex-shrink-0">
            <div className="flex items-center gap-2">
              <input
                ref={inputRef}
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask about debt restructuring..."
                disabled={isLoading}
                className="flex-1 text-sm px-4 py-2.5 rounded-xl border border-slate-200 bg-slate-50 focus:outline-none focus:ring-2 focus:ring-[#1e3a5f]/20 focus:border-[#1e3a5f]/30 disabled:opacity-50 placeholder:text-slate-400"
              />
              <Button
                onClick={handleSend}
                disabled={!input.trim() || isLoading}
                size="sm"
                className="gradient-navy hover:opacity-90 text-white rounded-xl h-10 w-10 p-0 flex-shrink-0"
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>
            <p className="text-[10px] text-slate-400 mt-2 text-center">
              AI-powered by Claude &middot; Based on verified IMF, World Bank &amp; Paris Club data
            </p>
          </div>
        </div>
      )}
    </>
  )
}

function formatChatMessage(text: string): string {
  const lines = text.split("\n")
  let html = ""
  let inList = false
  let listType: "ul" | "ol" | null = null

  for (const line of lines) {
    const trimmed = line.trim()
    if (!trimmed) {
      if (inList) { html += listType === "ul" ? "</ul>" : "</ol>"; inList = false; listType = null }
      continue
    }
    if (trimmed.startsWith("- ") || trimmed.startsWith("* ")) {
      if (!inList || listType !== "ul") {
        if (inList) html += listType === "ul" ? "</ul>" : "</ol>"
        html += "<ul>"; inList = true; listType = "ul"
      }
      html += `<li>${inlineMd(trimmed.slice(2))}</li>`; continue
    }
    const numMatch = trimmed.match(/^\d+\.\s+(.*)/)
    if (numMatch) {
      if (!inList || listType !== "ol") {
        if (inList) html += listType === "ul" ? "</ul>" : "</ol>"
        html += "<ol>"; inList = true; listType = "ol"
      }
      html += `<li>${inlineMd(numMatch[1])}</li>`; continue
    }
    if (inList) { html += listType === "ul" ? "</ul>" : "</ol>"; inList = false; listType = null }
    html += `<p>${inlineMd(trimmed)}</p>`
  }
  if (inList) html += listType === "ul" ? "</ul>" : "</ol>"
  return html
}

function inlineMd(t: string): string {
  return t.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
}
