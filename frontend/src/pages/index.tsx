import Head from "next/head";

export default function Home() {
  return (
    <>
      <Head>
        <title>Welcome | Your Next Big Thing</title>
        <meta name="description" content="Kickstarting your future project with Next.js and Tailwind" />
      </Head>
      <main className="min-h-screen flex flex-col items-center justify-center bg-gray-900 text-white px-4">
        <h1 className="text-4xl md:text-6xl font-bold text-center mb-6">
          This is the home of your future project.
        </h1>
        <p className="text-lg md:text-xl text-center max-w-2xl">
          A minimal starting point powered by <span className="text-blue-400">Next.js</span> and <span className="text-teal-400">Tailwind CSS</span>. Build something amazing!
        </p>
      </main>
    </>
  );
}
