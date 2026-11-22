# DocScan PDF — Escáner de Documentos y Unión PDF en Android

Aplicación web progresiva (**PWA**) sin dependencias externas que funciona directamente en el navegador y también puede **instalarse en tu teléfono Android** como una app nativa offline.

## Características principales

- **Galería múltiple y cámara en vivo (Ráfaga):** Selecciona varias imágenes ya guardadas en el teléfono de una sola vez o captura múltiples hojas seguidas con la cámara en tiempo real (disponible bajo HTTPS o `localhost`).
- **Realce de bordes de letras y limpieza de fondo (100% local en el dispositivo):**
  - **Documento Color:** Normalización morfológica por canal para eliminar sombras manteniendo firmas y sellos a color, seguida de un realce de bordes con máscara de enfoque selectiva (*edge-aware unsharp mask* con umbral antirruido).
  - **Texto Nítido B&N:** Limpieza de iluminación, realce reforzado de bordes de texto y curva de alto contraste sobre blanco puro.
  - **Alto Contraste (Sauvola):** Umbralización adaptativa local mediante imágenes integrales ($O(1)$ por píxel) con transición suavizada anti-escalonado para rescatar textos con sombras fuertes o poca luz.
  - **Grises:** Escala de grises limpia para documentos con gráficos o fotografías.
- **Recorte con corrección de perspectiva (4 esquinas):** Ajusta las 4 esquinas con lupa integrada para enderezar hojas fotografiadas en ángulo, rotación de 90° y comparación con el original.
- **Generación inmediata de PDF 1.4 dentro del teléfono:** Sin subir archivos a ningún servidor. Permite **Compartir** por WhatsApp/Correo/Drive o **Descargar** en tamaños A4, Carta o Ajustado.

## Cómo probarlo ahora mismo desde tu teléfono Android (Wi-Fi)

1. Conecta tu PC y tu teléfono a la **misma red Wi-Fi**.
2. En esta carpeta, ejecuta:
   ```bash
   python server.py
   ```
   *(Para habilitar el modo Ráfaga y la instalación PWA directa por Wi-Fi puedes usar `python server.py --https` y aceptar el certificado de prueba local en Chrome).*
3. Abre en Chrome de tu Android la dirección que muestra la consola (por ejemplo `http://192.168.1.X:8000`).

## Cómo instalarlo como App permanente offline en Android

Para instalarla permanentemente con Service Worker offline e ícono en tu pantalla de inicio (sin tener el PC encendido):

1. Sube esta carpeta (tal cual está, sin compilar nada) a cualquier hosting estático HTTPS gratuito como **Netlify Drop** (`app.netlify.com/drop`), **Cloudflare Pages** o **GitHub Pages**.
2. Abre la URL HTTPS en **Chrome en tu Android**.
3. Toca el botón **Instalar** dentro de la app (o menú **⋮ → Instalar aplicación**).
4. Listo: quedará instalada en Android y seguirá funcionando incluso en **Modo Avión / sin internet**.

## Cómo agregar varias fotos y actualizar la app en GitHub Pages

- **Varias fotos a la vez:** Toca **Subir varias fotos de galería** o **+ Galería (varias)**; en PC puedes seleccionar varios archivos con `Ctrl` / `Shift` o arrastrar varias imágenes directamente a la ventana. También puedes capturar múltiples hojas seguidas usando **Cámara en vivo (Ráfaga)** y luego tocar el botón central **Crear PDF**.
- **Si actualizas la app en GitHub Pages:** Si ya habías abierto una versión anterior en tu teléfono, recarga la página una vez con conexión a internet para que el Service Worker descargue la versión nueva.
