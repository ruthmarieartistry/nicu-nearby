import React, { useState } from "react";

export default function NICUFinder() {
  const [searchInput, setSearchInput] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await fetch(
        `/api/search-nicus?location=${encodeURIComponent(searchInput)}`,
      );
      const data = await response.json();
      if (response.ok) {
        setResults(data.results);
      } else {
        setError(data.error || "An error occurred");
      }
    } catch (err) {
      setError("Failed to fetch results");
    }
    setLoading(false);
  };

  return React.createElement(
    "div",
    { className: "container mx-auto p-4" },
    React.createElement(
      "h1",
      { className: "text-2xl font-bold mb-4" },
      "NICU Finder",
    ),
    React.createElement(
      "div",
      { className: "mb-4" },
      React.createElement("input", {
        type: "text",
        value: searchInput,
        onChange: (e) => setSearchInput(e.target.value),
        placeholder: "Enter location",
        className: "border p-2 mr-2",
      }),
      React.createElement(
        "button",
        {
          onClick: handleSearch,
          disabled: loading,
          className: "bg-blue-500 text-white p-2",
        },
        loading ? "Searching..." : "Search",
      ),
    ),
    error && React.createElement("p", { className: "text-red-500" }, error),
    React.createElement(
      "ul",
      { className: "list-disc pl-5" },
      results.map((result, index) =>
        React.createElement(
          "li",
          { key: index, className: "mb-2" },
          React.createElement("strong", null, result.name),
          " - ",
          result.address,
          " (",
          result.distance,
          ")",
        ),
      ),
    ),
  );
}
