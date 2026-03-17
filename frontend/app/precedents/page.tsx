import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { Breadcrumbs } from "@/components/breadcrumbs"
import { PrecedentsSearch } from "@/components/precedents-search"

export default function PrecedentsPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50">
      <Header />

      <main className="container mx-auto px-4 py-8">
        <Breadcrumbs />
        <PrecedentsSearch />
      </main>

      <Footer />
    </div>
  )
}
