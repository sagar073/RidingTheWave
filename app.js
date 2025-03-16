"use client";
import { useState } from "react";
import axios from "axios";
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";

export default function Dashboard() {
  const [url, setUrl] = useState("");
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileUpload = (e) => {
    setFile(e.target.files[0]);
  };

  const handleAnalyze = async () => {
    setLoading(true);
    const formData = new FormData();
    if (file) formData.append("file", file);
    if (url) formData.append("url", url);

    try {
      const response = await axios.post("http://127.0.0.1:5000/retrieve_classifications", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setData(response.data);
    } catch (error) {
      console.error("Error:", error);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold mb-6">🌱 SustainLens Dashboard</h1>

      <div className="bg-white p-4 rounded-lg shadow-md mb-6">
        <input
          type="text"
          placeholder="Enter Webpage URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="border p-2 rounded w-full mb-3"
        />
        <input type="file" onChange={handleFileUpload} className="mb-3" />
        <button onClick={handleAnalyze} className="bg-blue-500 text-white px-4 py-2 rounded">
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </div>

      {data && (
        <div className="bg-white p-4 rounded-lg shadow-md">
          <h2 className="text-xl font-bold mb-3">📊 Analysis Results</h2>
          <p><strong>Extracted Text:</strong> {data.text.slice(0, 300)}...</p>
          <p><strong>Keywords:</strong> {data.keywords.join(", ")}</p>
          <p><strong>SDG Classification:</strong> {data.sdg_classification}</p>

          {/* SDG Chart */}
          <div className="mt-6">
            <h3 className="text-lg font-bold">SDG Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={data.sdg_chart}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="sdg" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#4CAF50" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  );
}
