import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { Breadcrumbs } from "@/components/breadcrumbs"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { AlertTriangle, FileText, Database, Shield, Mail, Github, ExternalLink } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function LegalPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50">
      <Header />

      <div className="container mx-auto px-4 py-12 max-w-4xl">
        <Breadcrumbs />

        <div className="mb-12 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            Legal{" "}
            <span className="bg-gradient-to-r from-blue-600 to-blue-400 bg-clip-text text-transparent">
              Information
            </span>
          </h1>
          <p className="text-xl text-slate-600 max-w-3xl mx-auto">
            Disclaimer, terms of use, and data source attribution
          </p>
        </div>

        {/* Disclaimer */}
        <Card className="mb-8 border-amber-200 bg-amber-50/50">
          <CardHeader>
            <CardTitle className="flex items-center gap-3 text-amber-800">
              <AlertTriangle className="h-6 w-6" />
              Disclaimer
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4 text-slate-700">
            <p>
              <strong>This is a prototype platform for informational and educational purposes only.</strong>
              The information provided on this website does not constitute legal, financial, or professional advice.
            </p>
            <p>
              While data is sourced from official documents including IMF staff reports, Paris Club press releases, and
              World Bank publications, we cannot guarantee complete accuracy, timeliness, or reliability of all
              information. Data may contain errors, omissions, or may not reflect confidential terms of restructuring
              agreements.
            </p>
            <p>
              Users should independently verify all information with primary sources before making any decisions related
              to debt restructuring or financial matters. The creators and contributors of this platform accept no
              liability for any actions taken based on the information provided.
            </p>
          </CardContent>
        </Card>

        {/* Terms of Use */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-3 text-slate-800">
              <FileText className="h-6 w-6 text-blue-600" />
              Terms of Use
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4 text-slate-700">
            <div>
              <h3 className="font-semibold mb-2">Open Source License</h3>
              <p>
                This platform is an open-source project. You are free to use, modify, and distribute the code in
                accordance with the license terms in our GitHub repository.
              </p>
            </div>
            <div>
              <h3 className="font-semibold mb-2">No Warranties</h3>
              <p>
                This platform is provided "as is" without warranty of any kind, express or implied. We make no
                guarantees regarding availability, accuracy, or fitness for any particular purpose.
              </p>
            </div>
            <div>
              <h3 className="font-semibold mb-2">User Responsibility</h3>
              <p>
                Users are solely responsible for how they use the information and tools provided. Any decisions made
                based on this platform's data or analysis are the user's own responsibility.
              </p>
            </div>
            <div>
              <h3 className="font-semibold mb-2">Limitation of Liability</h3>
              <p>
                In no event shall the creators, contributors, or affiliates of this platform be liable for any direct,
                indirect, incidental, special, or consequential damages arising from the use of or inability to use this
                platform.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Data Sources */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-3 text-slate-800">
              <Database className="h-6 w-6 text-blue-600" />
              Data Sources & Attribution
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4 text-slate-700">
            <p>This platform aggregates publicly available data from the following official sources:</p>
            <ul className="space-y-3 ml-4">
              <li className="flex items-start gap-2">
                <div className="w-2 h-2 rounded-full bg-blue-500 mt-2 shrink-0" />
                <div>
                  <strong>World Bank</strong> - World Development Indicators (WDI), International Debt Statistics
                </div>
              </li>
              <li className="flex items-start gap-2">
                <div className="w-2 h-2 rounded-full bg-blue-500 mt-2 shrink-0" />
                <div>
                  <strong>International Monetary Fund (IMF)</strong> - World Economic Outlook (WEO), Debt Sustainability
                  Analyses, Staff Reports
                </div>
              </li>
              <li className="flex items-start gap-2">
                <div className="w-2 h-2 rounded-full bg-blue-500 mt-2 shrink-0" />
                <div>
                  <strong>Paris Club Secretariat</strong> - Official press releases and treatment terms
                </div>
              </li>
              <li className="flex items-start gap-2">
                <div className="w-2 h-2 rounded-full bg-blue-500 mt-2 shrink-0" />
                <div>
                  <strong>ND-GAIN</strong> - Notre Dame Global Adaptation Initiative Climate Vulnerability Index
                </div>
              </li>
              <li className="flex items-start gap-2">
                <div className="w-2 h-2 rounded-full bg-blue-500 mt-2 shrink-0" />
                <div>
                  <strong>Government Sources</strong> - Ministry of Finance publications and official announcements
                </div>
              </li>
            </ul>
            <p className="text-sm text-slate-500 mt-4">
              Data reflects publicly available information as of December 2024. We encourage users to consult primary
              sources for the most current information.
            </p>
          </CardContent>
        </Card>

        {/* Privacy Notice */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-3 text-slate-800">
              <Shield className="h-6 w-6 text-blue-600" />
              Privacy Notice
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4 text-slate-700">
            <p>
              This platform does not collect, store, or process personal user data. We do not use cookies for tracking
              purposes, and we do not require user registration.
            </p>
            <p>
              Any calculations or searches performed on this platform are processed in real-time and are not stored or
              logged. Your use of this platform is anonymous.
            </p>
          </CardContent>
        </Card>

        {/* Contact */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-3 text-slate-800">
              <Mail className="h-6 w-6 text-blue-600" />
              Get In Touch
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-slate-600 mb-6">
              Have questions, feedback, or interested in collaboration? Reach out through any of the channels below.
            </p>

            <div className="grid md:grid-cols-3 gap-4">
              {/* General Inquiries */}
              <div className="p-4 rounded-lg border border-slate-200 bg-slate-50/50 hover:border-blue-300 hover:bg-blue-50/50 transition-colors">
                <div className="flex items-center gap-2 mb-2">
                  <Mail className="h-5 w-5 text-blue-600" />
                  <h3 className="font-semibold text-slate-800">General Inquiries</h3>
                </div>
                <p className="text-sm text-slate-600 mb-3">Questions, feedback, or collaboration opportunities</p>
                <Button variant="outline" size="sm" className="w-full bg-transparent" asChild>
                  <a href="mailto:wanjiruanne95@gmail.com">Send Email</a>
                </Button>
              </div>

              {/* Technical / GitHub */}
              <div className="p-4 rounded-lg border border-slate-200 bg-slate-50/50 hover:border-blue-300 hover:bg-blue-50/50 transition-colors">
                <div className="flex items-center gap-2 mb-2">
                  <Github className="h-5 w-5 text-blue-600" />
                  <h3 className="font-semibold text-slate-800">Technical Issues</h3>
                </div>
                <p className="text-sm text-slate-600 mb-3">Bug reports, feature requests, or code contributions</p>
                <Button variant="outline" size="sm" className="w-full bg-transparent" asChild>
                  <a href="https://github.com/AnneNgarachu/Borrowers-Forum" target="_blank" rel="noopener noreferrer">
                    GitHub Repo
                    <ExternalLink className="h-3 w-3 ml-1" />
                  </a>
                </Button>
              </div>

              {/* Portfolio */}
              <div className="p-4 rounded-lg border border-slate-200 bg-slate-50/50 hover:border-blue-300 hover:bg-blue-50/50 transition-colors">
                <div className="flex items-center gap-2 mb-2">
                  <ExternalLink className="h-5 w-5 text-blue-600" />
                  <h3 className="font-semibold text-slate-800">About the Developer</h3>
                </div>
                <p className="text-sm text-slate-600 mb-3">Learn more about the developer and other projects</p>
                <Button variant="outline" size="sm" className="w-full bg-transparent" asChild>
                  <a href="https://annengarachu.com" target="_blank" rel="noopener noreferrer">
                    Visit Portfolio
                    <ExternalLink className="h-3 w-3 ml-1" />
                  </a>
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        <div className="text-center text-sm text-slate-500 mt-12">
          <p>Last updated: January 2025</p>
        </div>
      </div>

      <Footer />
    </div>
  )
}
