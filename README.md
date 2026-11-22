# DocScan PDF — Escáner de Documentos y Unión PDF en Android

Aplicación web progresiva (**PWA**) 100% autocontenida en un único `index.html` (sin dependencias externas ni subcarpetas) que funciona directamente en el navegador y puede **instalarse en tu teléfono Android** como una app offline.

## Características principales

- **Galería múltiple y cámara en vivo (Ráfaga):** Selecciona varias imágenes guardadas en el teléfono de una sola vez o captura múltiples hojas seguidas con la cámara en tiempo real (disponible bajo HTTPS o `localhost`).
- **Realce de bordes de letras y limpieza de fondo (100% local en el dispositivo):**
  - **Documento Color:** Normalización morfológica por canal para eliminar sombras manteniendo firmas y sellos a color, seguida de un realce de bordes con máscara de enfoque selectiva (*edge-aware unsharp mask* con umbral antirruido).
  - **Texto Nítido B&N:** Limpieza de iluminación, realce reforzado de bordes de texto y curva de alto contraste sobre blanco puro.
  - **Alto Contraste (Sauvola):** Umbralización adaptativa local mediante imágenes integrales ($O(1)$ por píxel) con transición suavizada anti-escalonado para rescatar textos con sombras fuertes o poca luz.
  - **Grises:** Escala de grises limpia para documentos con gráficos o fotografías.
- **Recorte con corrección de perspectiva (4 esquinas):** Ajusta las 4 esquinas con lupa integrada para enderezar hojas fotografiadas en ángulo, rotación de 90° y comparación con el original.
- **Generación inmediata de PDF 1.4 dentro del teléfono:** Sin subir archivos a ningún servidor. Permite **Descargar** o **Compartir** en tamaños A4, Carta o Ajustado.

## Subir a GitHub Pages (sin subcarpetas)

No hay ninguna subcarpeta que subir: todos los archivos están en la raíz del proyecto (`index.html`, `manifest.json`, `sw.js`, `icon-192.png`, `icon-512.png`). Incluso subiendo únicamente `index.html` por la web de GitHub la aplicación funciona por completo; subir además `manifest.json`, `sw.js`, `icon-192.png` e `icon-512.png` habilita la instalación PWA offline en Android.

1. Sube estos archivos de la raíz a tu repositorio de GitHub y activa GitHub Pages.
2. Abre la URL HTTPS en **Chrome en tu Android** (si habías abierto una versión anterior, recarga hasta ver **`Escáner local • v4`** debajo del título).
3. Toca **Instalar** (o menú **⋮ → Instalar aplicación**) para usarla sin internet.

## Cómo probarlo en red local (Wi-Fi)

```bash
python server.py
```
*(Usa `python server.py --https` para probar también la cámara en vivo por Wi-Fi).*
