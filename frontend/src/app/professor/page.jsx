"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import {
  onAuthStateChanged,
  signOut
} from "firebase/auth";

import { auth } from "../../lib/firebase";


export default function ProfessorDashboard() {

  const router = useRouter();

  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);


  useEffect(() => {

    const unsubscribe = onAuthStateChanged(
      auth,
      (currentUser) => {

        if (!currentUser) {

          router.push("/login");

        } else {

          setUser(currentUser);

        }

        setLoading(false);

      }
    );

    return () => unsubscribe();

  }, [router]);


  const handleLogout = async () => {

    await signOut(auth);

    router.push("/login");

  };


  if (loading) {

    return (
      <div className="min-h-screen flex items-center justify-center">
        Loading...
      </div>
    );

  }


  return (

    <main className="min-h-screen bg-gray-100 p-8">

      <div className="max-w-6xl mx-auto">


        {/* HEADER */}

        <div className="flex justify-between items-center mb-8">

          <div>

            <h1 className="text-3xl font-bold">
              Professor Dashboard
            </h1>

            <p className="text-gray-600">

              Welcome, {user?.email}

            </p>

          </div>


          <button
            onClick={handleLogout}
            className="bg-red-500 text-white px-5 py-2 rounded-lg"
          >

            Logout

          </button>

        </div>


        {/* DASHBOARD CARDS */}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">


          <div className="bg-white p-6 rounded-xl shadow">

            <h2 className="text-xl font-bold">
              Student Submissions
            </h2>

            <p className="text-gray-500 mt-2">
              View student submissions.
            </p>

          </div>


          <div className="bg-white p-6 rounded-xl shadow">

            <h2 className="text-xl font-bold">
              AI Provenance Check
            </h2>

            <p className="text-gray-500 mt-2">
              Analyze AI-generated content.
            </p>

          </div>


          <div className="bg-white p-6 rounded-xl shadow">

            <h2 className="text-xl font-bold">
              Reports
            </h2>

            <p className="text-gray-500 mt-2">
              View analysis reports.
            </p>

          </div>


        </div>

      </div>

    </main>

  );
}