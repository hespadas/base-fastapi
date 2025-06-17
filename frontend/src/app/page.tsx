export const metadata = {
  title: "Welcome | Your Next Big Thing",
  description: "Kickstarting your future project with Next.js and Tailwind",
};

export default function Home() {
  return (
    <main className="flex flex-col min-h-screen items-center justify-center bg-gray-50 px-4">
      <header className="w-full max-w-4xl flex flex-col items-center py-16">
        <h1 className="text-5xl md:text-6xl font-extrabold text-gray-900 mb-4 text-center">
          Show Your Progress
        </h1>
        <p className="text-xl text-gray-600 text-center mb-8 max-w-2xl">
          The Site to track, showcase, and celebrate your progress — as an individual, a team, or a whole community!
        </p>
        <div className="flex flex-col sm:flex-row gap-4">
          <a
            href="/signup"
            className="px-8 py-3 bg-blue-600 text-white rounded-2xl shadow-md font-semibold hover:bg-blue-700 transition"
          >
            Get Started
          </a>
        </div>
      </header>

      <footer className="w-full py-8 text-center text-gray-400">
        &copy; {new Date().getFullYear()} ShowYourProgress. All rights reserved.
      </footer>
    </main>
  );
}
