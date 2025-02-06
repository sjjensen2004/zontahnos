"use client";

import { useState } from "react";
import { Calendar } from "@/components/ui/calendar";

export default function Home() {
  // State to store the selected date
  const [date, setDate] = useState<Date | undefined>(undefined);

  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-4">
      <h1 className="text-2xl font-bold mb-4">UI Test</h1>

      <Calendar
        mode="single"
        selected={date}
        onSelect={setDate} // Updates the state
        className="rounded-md border"
      />

      {/* Display selected date */}
      {date && <p className="mt-4 text-lg">Selected Date: {date.toDateString()}</p>}
    </main>
  );
}