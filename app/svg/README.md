# SVG Controls para PyQt5 Interface

Esta carpeta contiene controles SVG personalizados para la interfaz PyQt5 del bot Gabo AI.

## Controles Disponibles

### Botones

#### `button-primary.svg`
- **Uso**: Botones principales de acción
- **Características**: Gradiente azul, sombra, efecto de resplandor
- **Estados**: Normal, hover, pressed
- **Dimensiones**: 120x40px

#### `button-secondary.svg`
- **Uso**: Botones secundarios y de navegación
- **Características**: Estilo outline, gradiente gris
- **Estados**: Normal, hover
- **Dimensiones**: 120x40px

#### `button-danger.svg`
- **Uso**: Acciones destructivas y de advertencia
- **Características**: Gradiente rojo, rayas de advertencia
- **Estados**: Normal, hover
- **Dimensiones**: 120x40px

### Campos de Entrada

#### `input-field.svg`
- **Uso**: Campos de texto y entrada
- **Características**: Gradiente blanco, borde de foco
- **Estados**: Normal, focus, hover
- **Dimensiones**: 200x50px

### Controles de Selección

#### `checkbox.svg`
- **Uso**: Casillas de verificación
- **Características**: Bordes redondeados, marca de verificación
- **Estados**: Unchecked, checked, hover
- **Dimensiones**: 24x24px

#### `radio-button.svg`
- **Uso**: Botones de opción
- **Características**: Diseño circular, punto de selección
- **Estados**: Unselected, selected, hover
- **Dimensiones**: 24x24px

### Controles de Progreso

#### `progress-bar.svg`
- **Uso**: Barras de progreso
- **Características**: Gradiente multicolor, rayas animadas
- **Estados**: 0%, 25%, 50%, 75%, 100%
- **Dimensiones**: 200x20px

#### `slider-track.svg`
- **Uso**: Controles deslizantes
- **Características**: Pista con marcadores, pulgar deslizante
- **Estados**: Min, max, valor actual
- **Dimensiones**: 200x24px

### Navegación

#### `tab-button.svg`
- **Uso**: Botones de pestañas
- **Características**: Indicador de estado activo, borde superior
- **Estados**: Inactive, active, hover
- **Dimensiones**: 120x40px

### Contenedores

#### `group-box.svg`
- **Uso**: Agrupación de controles
- **Características**: Área de título, contenido estructurado
- **Estados**: Normal, expanded, collapsed
- **Dimensiones**: 300x200px

### Indicadores

#### `status-indicator.svg`
- **Uso**: Indicadores de estado del sistema
- **Características**: Estados múltiples (success, warning, error, info)
- **Estados**: Success, warning, error, info
- **Dimensiones**: 24x24px

#### `tooltip.svg`
- **Uso**: Información contextual
- **Características**: Flecha apuntadora, fondo oscuro
- **Estados**: Visible, hidden
- **Dimensiones**: 200x80px

## Uso en PyQt5

### Cargar SVG como Icono
```python
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

# Cargar SVG como icono
button = QPushButton("Mi Botón")
button.setIcon(QIcon("app/svg/button-primary.svg"))
```

### Cargar SVG como Pixmap
```python
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

# Cargar SVG como imagen
label = QLabel()
pixmap = QPixmap("app/svg/status-indicator.svg")
label.setPixmap(pixmap)
```

### Aplicar Estilos CSS
```python
# Usar SVG en estilos CSS
button.setStyleSheet("""
QPushButton {
    background-image: url(app/svg/button-primary.svg);
    border: none;
    padding: 10px 20px;
}
""")
```

### Crear Controles Personalizados
```python
class CustomButton(QPushButton):
    def __init__(self, text, svg_path):
        super().__init__(text)
        self.svg_path = svg_path
        self.load_svg()
    
    def load_svg(self):
        # Cargar SVG y aplicar estilos
        self.setIcon(QIcon(self.svg_path))
        self.setIconSize(QSize(120, 40))
```

## Personalización

### Cambiar Colores
Los SVGs usan variables CSS que se pueden modificar:
- `#4F46E5` - Color primario (azul)
- `#3730A3` - Color primario oscuro
- `#EF4444` - Color de peligro (rojo)
- `#10B981` - Color de éxito (verde)
- `#F59E0B` - Color de advertencia (amarillo)

### Modificar Tamaños
Todos los SVGs usan `viewBox` que permite escalado sin pérdida de calidad:
```python
# Escalar a cualquier tamaño
pixmap = QPixmap("app/svg/button-primary.svg")
scaled_pixmap = pixmap.scaled(240, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
```

### Estados Interactivos
Los SVGs incluyen elementos para diferentes estados:
- **Normal**: Opacidad 1.0
- **Hover**: Opacidad 0.8
- **Pressed**: Opacidad 0.6
- **Disabled**: Opacidad 0.3

## Optimización

### Comprimir SVGs
```bash
# Usar svgo para optimizar
npm install -g svgo
svgo app/svg/*.svg
```

### Convertir a PNG (si es necesario)
```python
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtGui import QPainter, QPixmap

def svg_to_png(svg_path, png_path, size):
    renderer = QSvgRenderer(svg_path)
    pixmap = QPixmap(size)
    pixmap.fill(Qt.transparent)
    
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    
    pixmap.save(png_path)
```

## Compatibilidad

- **PyQt5**: ✅ Totalmente compatible
- **PyQt6**: ✅ Compatible (requiere ajustes menores)
- **PySide2**: ✅ Compatible
- **PySide6**: ✅ Compatible

## Notas de Diseño

- Todos los controles usan **Material Design** como base
- **Bordes redondeados** para un look moderno
- **Sombras sutiles** para profundidad
- **Gradientes** para visual atractivo
- **Estados múltiples** para interactividad
- **Escalado vectorial** para cualquier resolución

## Licencia

Los SVGs están bajo la misma licencia GPL-2.0-or-later que el proyecto principal.
