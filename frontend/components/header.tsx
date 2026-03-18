"use client"

import { Globe, Menu, X } from "lucide-react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { useState } from "react"
import { cn } from "@/lib/utils"

export function Header() {
  const pathname = usePathname()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const navItems = [
    { href: "/", label: "Home" },
    { href: "/calculator", label: "Calculator" },
    { href: "/precedents", label: "Precedents" },
    { href: "/countries", label: "Countries" },
    { href: "/about", label: "About" },
  ]

  return (
    <header className="border-b border-[#1e3a5f]/10 bg-gradient-to-r from-slate-50 via-blue-50/50 to-slate-50 sticky top-0 z-50 backdrop-blur-sm shadow-sm">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-3 hover:opacity-80 transition-opacity group">
            <div className="bg-[#1e3a5f]/10 p-2 rounded-lg backdrop-blur-sm border border-[#1e3a5f]/20 group-hover:bg-[#1e3a5f]/15 transition-colors">
              <Globe className="h-6 w-6 text-[#1e3a5f]" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight text-[#1e3a5f]">The Borrower&apos;s Forum</h1>
              <p className="text-xs text-slate-500">Debt Intelligence Platform</p>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-1">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "px-4 py-2 rounded-md text-sm font-medium transition-colors",
                  pathname === item.href
                    ? "bg-[#1e3a5f]/10 text-[#1e3a5f] border border-[#1e3a5f]/20 font-semibold"
                    : "text-slate-600 hover:text-[#1e3a5f] hover:bg-[#1e3a5f]/5",
                )}
              >
                {item.label}
              </Link>
            ))}
          </nav>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden p-2 rounded-md text-slate-600 hover:bg-[#1e3a5f]/5 transition-colors"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label={mobileMenuOpen ? "Close menu" : "Open menu"}
          >
            {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <nav className="md:hidden mt-4 pb-2 border-t border-[#1e3a5f]/10 pt-4 space-y-1">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setMobileMenuOpen(false)}
                className={cn(
                  "block px-4 py-3 rounded-md text-sm font-medium transition-colors",
                  pathname === item.href
                    ? "bg-[#1e3a5f]/10 text-[#1e3a5f] font-semibold"
                    : "text-slate-600 hover:text-[#1e3a5f] hover:bg-[#1e3a5f]/5",
                )}
              >
                {item.label}
              </Link>
            ))}
          </nav>
        )}
      </div>
    </header>
  )
}
