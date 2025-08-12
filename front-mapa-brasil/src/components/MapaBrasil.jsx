import React, { useEffect, useState } from "react";
import { ComposableMap, Geographies, Geography } from "react-simple-maps";
import axios from "axios";

const geoUrl =
  "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson";

export default function MapaBrasil() {
  const [dados, setDados] = useState({});
  const [tooltip, setTooltip] = useState("");
  const [anoSelecionado, setAnoSelecionado] = useState("2023");
  const [estadoSelecionado, setEstadoSelecionado] = useState(null);
  const [nomeEstadoSelecionado, setNomeEstadoSelecionado] = useState("");

  useEffect(() => {
    const url =
      anoSelecionado === "all"
        ? "http://localhost:5000/censoescolar?ano=all"
        : `http://localhost:5000/censoescolar?ano=${anoSelecionado}`;

    axios
      .get(url)
      .then((res) => setDados(res.data))
      .catch((err) => console.error("Erro na API:", err));
  }, [anoSelecionado]);

  const valores = Object.values(dados);
  const totalMatriculas = valores.reduce((acc, curr) => acc + curr, 0);
  const maxValor = Math.max(...valores, 1);

  const getColor = (valor) => {
    const percent = valor / maxValor;
    const lightness = 80 - percent * 60;
    return `hsl(220, 100%, ${lightness}%)`;
  };

  return (
    <div
      style={{
        width: "100%",
        height: "100vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        backgroundColor: "#121212",
        color: "#fff",
      }}
    >
      <h1>Sistema de Estados</h1>

      <select
        value={anoSelecionado}
        onChange={(e) => {
          setAnoSelecionado(e.target.value);
          setEstadoSelecionado(null);
        }}
        style={{
          marginBottom: "10px",
          padding: "8px 12px",
          borderRadius: "5px",
          fontSize: "16px",
        }}
      >
        <option value="2023">Ano 2023</option>
        <option value="2024">Ano 2024</option>
        <option value="all">Total 2023 e 2024</option>
      </select>

      <p style={{ marginBottom: "20px" }}>
        Total de Matrículas{" "}
        {anoSelecionado === "all" ? "2023 e 2024" : `em ${anoSelecionado}`}:{" "}
        {totalMatriculas.toLocaleString()}
      </p>

      <ComposableMap
        projection="geoMercator"
        projectionConfig={{ scale: 600, center: [-55, -15] }}
        style={{
          width: "100%",
          height: "auto",
          maxWidth: "800px",
        }}
      >
        <Geographies geography={geoUrl}>
          {({ geographies }) => {
            return (
              <>
                {geographies.map((geo) => {
                  const sigla = geo.properties.sigla;
                  const nome = geo.properties.name;
                  const valor = dados[sigla] || 0;

                  if (sigla === estadoSelecionado) return null;

                  return (
                    <Geography
                      key={geo.rsmKey}
                      geography={geo}
                      fill={getColor(valor)}
                      stroke="#FFF"
                      strokeWidth={0.5}
                      onMouseEnter={() =>
                        setTooltip(`${nome} - ${valor.toLocaleString()} matrículas`)
                      }
                      onMouseLeave={() => setTooltip("")}
                      onClick={() => {
                        setEstadoSelecionado(sigla);
                        setNomeEstadoSelecionado(nome);
                      }}
                      style={{
                        default: {
                          outline: "none",
                          opacity: estadoSelecionado ? 0.3 : 1,
                          transition: "all 0.3s ease",
                        },
                        hover: { fill: "#f39c12", outline: "none" },
                        pressed: { outline: "none" },
                      }}
                    />
                  );
                })}

                {estadoSelecionado &&
                  geographies
                    .filter((geo) => geo.properties.sigla === estadoSelecionado)
                    .map((geo) => {
                      const sigla = geo.properties.sigla;
                      const nome = geo.properties.name;
                      const valor = dados[sigla] || 0;

                      return (
                        <Geography
                          key={geo.rsmKey + "-selected"}
                          geography={geo}
                          fill={getColor(valor)}
                          stroke="#FFD700"
                          strokeWidth={2}
                          onMouseEnter={() =>
                            setTooltip(`${nome} - ${valor.toLocaleString()} matrículas`)
                          }
                          onMouseLeave={() => setTooltip("")}
                          onClick={() => {
                            setEstadoSelecionado(null);
                            setNomeEstadoSelecionado("");
                          }}
                          style={{
                            default: {
                              outline: "none",
                              transform: "scale(1.04) translateY(-4px)",
                              transition: "all 0.3s ease",
                              filter: "drop-shadow(0px 0px 8px rgba(255, 215, 0, 0.5))",
                            },
                            hover: { fill: "#f39c12", outline: "none" },
                            pressed: { outline: "none" },
                          }}
                        />
                      );
                    })}
              </>
            );
          }}
        </Geographies>
      </ComposableMap>

      {tooltip && (
        <div
          style={{
            position: "fixed",
            bottom: 20,
            backgroundColor: "#ffffff",
            padding: "5px 10px",
            borderRadius: "5px",
            color: "#000",
          }}
        >
          {tooltip}
        </div>
      )}

      {estadoSelecionado && (
        <div
          style={{
            position: "fixed",
            right: 20,
            top: 20,
            backgroundColor: "#fff",
            color: "#000",
            padding: "15px 20px",
            borderRadius: "10px",
            boxShadow: "0px 0px 15px rgba(0,0,0,0.3)",
            zIndex: 10,
            minWidth: "250px",
          }}
        >
          <h3>{nomeEstadoSelecionado}</h3>
          <p>
            Matrículas em {anoSelecionado === "all" ? "2023 + 2024" : anoSelecionado}:{" "}
            <strong>{dados[estadoSelecionado].toLocaleString()}</strong>
          </p>
          <button
            onClick={() => setEstadoSelecionado(null)}
            style={{
              marginTop: "10px",
              padding: "5px 10px",
              background: "#f39c12",
              border: "none",
              borderRadius: "5px",
              color: "#fff",
              cursor: "pointer",
            }}
          >
            Fechar
          </button>
        </div>
      )}
    </div>
  );
}
